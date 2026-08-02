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
    case = await auth.case_owned_by(case_id, user)
    row = await db.fetchrow(
        "select answers from form_data where case_id=$1", case["id"]
    )
    answers = dict(row["answers"]) if row else {}
    emp = answers.get("current_employer") or {}
    work_state = (emp.get("state") if isinstance(emp, dict) else None) \
        or answers.get("mailing.state")
    return {
        "sections": forms_spec.WIZARD,
        "forms": list(formfill.FORM_SOURCES.keys()),
        "fees": forms_spec.FEES,
        "lockbox_note": forms_spec.LOCKBOX_NOTE,
        "filing_address": forms_spec.filing_address(
            work_state, premium=answers.get("processing.premium") is True
        ),
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
        ans_row = await db.fetchrow(
            "select answers from form_data where case_id=$1", cid
        )
        answers = dict(ans_row["answers"]) if ans_row else {}
        premium = answers.get("processing.premium") is True
        emp = answers.get("current_employer") or {}
        work_state = (emp.get("state") if isinstance(emp, dict) else None) \
            or answers.get("mailing.state")
        addr = forms_spec.filing_address(work_state, premium=premium)
        fee_line = (
            f"I-140 fee ${forms_spec.FEES['i-140']} + Asylum Program Fee "
            f"${forms_spec.FEES['asylum_program_fee_self']} (self-petitioner)"
        )
        if premium:
            fee_line += (
                f"; I-907 premium fee ${forms_spec.FEES['i-907_premium']} on "
                "its OWN payment form (one payment per form)"
            )
        items = [
            "Fee payment: G-1650 (ACH, recommended) or G-1450 (credit card; "
            "a declined card rejects the whole package) — " + fee_line,
            "G-1145 e-notification",
            *(["Form I-907 premium processing request (signed)"] if premium
              else []),
            "Cover letter, marked 'Original Submission — Form I-140' (mark "
            "the envelope the same way)",
            "Form I-140 (signed in black ink)",
            "ETA-9089 Appendix A + signed Final Determination (as a "
            "self-petitioner you sign BOTH the petitioner and the "
            "beneficiary blocks; wet signatures)",
            "Foreign name & address page — your name and foreign address in "
            "your native alphabet (only if it is non-Roman; not needed if "
            "born in India)",
            "Identity documents: passport pages with stamps (no blank "
            "pages), current status approval notice, I-94 front and back",
            "Petition Letter",
            "Proposed Endeavor Statement (signed)",
            "Support letters (signed, on letterhead) — put each "
            "recommender's CV (max 5 pages) or a printed bio page behind "
            "their letter",
            "Exhibits in the order of the Index of Exhibits (publications: "
            "first 3-5 pages of each paper are enough; highlight your name "
            "in the author list)",
        ]
        order = "\n".join(f"{i}. {t}" for i, t in enumerate(items, 1))
        readme = (
            "OPENNIW FILING PACKAGE\n======================\n\n"
            "Assembly order (top to bottom — USCIS-recommended: payment "
            "form first):\n"
            + order + "\n\n"
            f"MAIL TO — {addr['name']}:\n"
            f"USPS:\n{addr['usps']}\n\n"
            f"FedEx/UPS/DHL:\n{addr['courier']}\n"
            f"({addr['note']})\n"
            "If you file I-485 concurrently in the same envelope (no "
            "premium), the address differs: Dallas Lockbox, Attn: NFB.\n\n"
            + forms_spec.LOCKBOX_NOTE
            + "\n\nAny document in a foreign language needs a full English "
            "translation plus the translator's signed certification that "
            "the translation is complete and accurate and that they are "
            "competent to translate. Keep a complete copy of the package. "
            "This package was prepared with OpenNIW, an open-source "
            "document preparation tool. It is not legal advice; review "
            "everything before filing.\n"
        )
        zf.writestr("README.txt", readme)
    buf.seek(0)
    return Response(
        content=buf.getvalue(), media_type="application/zip",
        headers={"Content-Disposition":
                 'attachment; filename="openniw-package.zip"'},
    )
