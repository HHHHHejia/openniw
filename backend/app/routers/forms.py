import io
import json
import uuid
import zipfile

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel

from .. import auth, db
from ..services import docx_export, formfill, forms_spec, llm, storage

router = APIRouter(prefix="/api/cases/{case_id}/forms", tags=["forms"])


class AnswersUpdate(BaseModel):
    answers: dict


@router.get("/spec")
async def spec(case_id: str, user: dict = Depends(auth.current_user)) -> dict:
    await auth.case_owned_by(case_id, user)
    return {
        "sections": forms_spec.WIZARD,
        "forms": list(formfill.FORM_SOURCES.keys()),
        "fees": forms_spec.FEES,
        "lockbox_note": forms_spec.LOCKBOX_NOTE,
    }


@router.get("/answers")
async def get_answers(case_id: str, user: dict = Depends(auth.current_user)) -> dict:
    case = await auth.case_owned_by(case_id, user)
    row = await db.fetchrow(
        "select answers from form_data where case_id=$1", case["id"]
    )
    return {"answers": dict(row["answers"]) if row else {}}


@router.put("/answers")
async def put_answers(
    case_id: str, body: AnswersUpdate, user: dict = Depends(auth.current_user)
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    await db.execute(
        """insert into form_data(case_id, answers) values($1,$2)
           on conflict (case_id) do update set answers=$2, updated_at=now()""",
        case["id"], body.answers,
    )
    return {"ok": True}


@router.post("/prefill")
async def prefill(case_id: str, user: dict = Depends(auth.current_user)) -> dict:
    """AI pass: derive whatever wizard answers we can from the case profile."""
    case = await auth.case_owned_by(case_id, user)
    profile = await db.fetchrow(
        "select parsed from profiles where case_id=$1", case["id"]
    )
    existing = await db.fetchrow(
        "select answers from form_data where case_id=$1", case["id"]
    )
    keys = [
        f["key"] for section in forms_spec.WIZARD for f in section["fields"]
    ]
    result = await llm.complete(
        "From this applicant profile, pre-fill as many of these form-wizard "
        "answers as the data supports. Keys use dotted paths; 'degrees' is a "
        "list of {level, field, institution, country, month_year}; "
        "'current_employer' is {name, address1, city, state, postal_code, "
        "country, job_title, start, hours_per_week, duties}; 'family' is a "
        "list of {family_name, given_name, dob, country_of_birth, "
        "relationship}. Only include keys you can support from the data — "
        "NEVER guess identity numbers, dates, or addresses.\n\nKEYS:\n"
        + json.dumps(keys)
        + "\n\nPROFILE:\n"
        + json.dumps(dict(profile["parsed"]) if profile else {},
                     ensure_ascii=False)[:60000],
        schema={"type": "object"},
        effort="medium",
    )
    merged = {**(result or {}), **(dict(existing["answers"]) if existing else {})}
    await db.execute(
        """insert into form_data(case_id, answers) values($1,$2)
           on conflict (case_id) do update set answers=$2, updated_at=now()""",
        case["id"], merged,
    )
    return {"answers": merged}


@router.post("/fill/{form_code}")
async def fill_form(
    case_id: str, form_code: str, user: dict = Depends(auth.current_user)
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    if form_code not in formfill.FORM_SOURCES:
        raise HTTPException(404, f"Unknown form {form_code}")
    row = await db.fetchrow(
        "select answers from form_data where case_id=$1", case["id"]
    )
    answers = dict(row["answers"]) if row else {}
    pdf_bytes, report = formfill.fill(form_code, answers)
    rel = storage.save(str(case["id"]), f"{form_code}-filled.pdf", pdf_bytes)
    filled_id = await db.fetchval(
        """insert into filled_forms(case_id, form_code, file_path)
           values($1,$2,$3) returning id""",
        case["id"], form_code, rel,
    )
    return {"id": str(filled_id), "report": report}


@router.get("/filled")
async def list_filled(
    case_id: str, user: dict = Depends(auth.current_user)
) -> list[dict]:
    case = await auth.case_owned_by(case_id, user)
    rows = await db.fetch(
        """select distinct on (form_code) id, form_code, created_at
           from filled_forms where case_id=$1 order by form_code, created_at desc""",
        case["id"],
    )
    return [
        {"id": str(r["id"]), "form_code": r["form_code"],
         "created_at": r["created_at"].isoformat()}
        for r in rows
    ]


@router.get("/filled/{filled_id}/pdf")
async def download_filled(
    case_id: str, filled_id: str, user: dict = Depends(auth.current_user)
) -> Response:
    case = await auth.case_owned_by(case_id, user)
    row = await db.fetchrow(
        "select * from filled_forms where id=$1 and case_id=$2",
        uuid.UUID(filled_id), case["id"],
    )
    if row is None:
        raise HTTPException(404, "Not found")
    data = storage.read(row["file_path"])
    return Response(
        content=data, media_type="application/pdf",
        headers={"Content-Disposition":
                 f'attachment; filename="{row["form_code"]}.pdf"'},
    )


@router.get("/package")
async def package_zip(
    case_id: str, user: dict = Depends(auth.current_user)
) -> Response:
    """One ZIP: filled forms + finalized documents as DOCX + assembly README."""
    case = await auth.case_owned_by(case_id, user)
    cid = case["id"]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        forms = await db.fetch(
            """select distinct on (form_code) form_code, file_path
               from filled_forms where case_id=$1 order by form_code, created_at desc""",
            cid,
        )
        for f in forms:
            try:
                zf.writestr(f"forms/{f['form_code']}.pdf",
                            storage.read(f["file_path"]))
            except Exception:
                continue
        docs = await db.fetch(
            """select distinct on (doc_type, recommender_id)
                 doc_type, recommender_id, version, content_md
               from documents where case_id=$1
               order by doc_type, recommender_id, version desc""",
            cid,
        )
        for d in docs:
            name = d["doc_type"]
            if d["recommender_id"]:
                name += f"_{str(d['recommender_id'])[:8]}"
            zf.writestr(
                f"documents/{name}.docx",
                docx_export.markdown_to_docx(d["content_md"]),
            )
        readme = (
            "OPENNIW FILING PACKAGE\n======================\n\n"
            "Assembly order (top to bottom):\n"
            "1. G-1145 e-notification (clipped on top)\n"
            "2. Fee payment: G-1650 (ACH, recommended) or G-1450 — I-140 fee "
            f"${forms_spec.FEES['i-140']} + Asylum Program Fee "
            f"${forms_spec.FEES['asylum_program_fee_self']} (self-petitioner)\n"
            "3. Form I-140 (signed in black ink)\n"
            "4. ETA-9089 Appendix A + signed Final Determination page\n"
            "5. Petition Letter\n"
            "6. Proposed Endeavor Statement (signed)\n"
            "7. Support letters (signed, on letterhead)\n"
            "8. Exhibits in the order of the Index of Exhibits\n\n"
            + forms_spec.LOCKBOX_NOTE
            + "\n\nPrint single-sided. No staples. This package was prepared "
            "with OpenNIW, an open-source document preparation tool. It is "
            "not legal advice; review everything before filing.\n"
        )
        zf.writestr("README.txt", readme)
    buf.seek(0)
    return Response(
        content=buf.getvalue(), media_type="application/zip",
        headers={"Content-Disposition":
                 'attachment; filename="openniw-package.zip"'},
    )
