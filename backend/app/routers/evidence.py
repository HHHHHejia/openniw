import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel

from .. import auth, db
from ..services import evidence_intake, jobs, scraping, storage

router = APIRouter(prefix="/api/cases/{case_id}/evidence", tags=["evidence"])


class EvidenceUpdate(BaseModel):
    status: str | None = None
    title: str | None = None
    description: str | None = None
    source_url: str | None = None
    ai_notes: str | None = None
    exhibit_no: int | None = None


class EvidenceCreate(BaseModel):
    category: str
    title: str
    description: str | None = None
    status: str = "needed"


@router.get("")
async def list_items(
    case_id: str, user: dict = Depends(auth.current_user)
) -> list[dict]:
    case = await auth.case_owned_by(case_id, user)
    rows = await db.fetch(
        "select * from evidence_items where case_id=$1 order by category, created_at",
        case["id"],
    )
    return [
        {
            **{k: r[k] for k in (
                "category", "title", "description", "status", "source_url",
                "ai_notes", "exhibit_no", "date_class",
            )},
            "id": str(r["id"]),
            "has_file": r["file_path"] is not None,
            "doc_kind": (r["extracted"] or {}).get("doc_kind"),
        }
        for r in rows
    ]


@router.post("")
async def add_item(
    case_id: str, body: EvidenceCreate, user: dict = Depends(auth.current_user)
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    item_id = await db.fetchval(
        """insert into evidence_items(case_id, category, title, description, status)
           values($1,$2,$3,$4,$5) returning id""",
        case["id"], body.category, body.title, body.description, body.status,
    )
    return {"id": str(item_id)}


@router.put("/{item_id}")
async def update_item(
    case_id: str, item_id: str, body: EvidenceUpdate,
    user: dict = Depends(auth.current_user),
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    if not updates:
        return {"ok": True}
    sets = ", ".join(f"{k}=${i + 3}" for i, k in enumerate(updates))
    result = await db.execute(
        f"update evidence_items set {sets} where id=$1 and case_id=$2",
        uuid.UUID(item_id), case["id"], *updates.values(),
    )
    if result.endswith("0"):
        raise HTTPException(404, "Evidence item not found")
    return {"ok": True}


@router.post("/{item_id}/file")
async def upload_file(
    case_id: str, item_id: str, background: BackgroundTasks,
    file: UploadFile = File(...),
    user: dict = Depends(auth.current_user),
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    content = await file.read()
    if len(content) > 50 * 1024 * 1024:
        raise HTTPException(413, "File too large (50 MB max)")
    rel = storage.save(str(case["id"]), file.filename or "evidence", content)
    text = None
    if (file.filename or "").lower().endswith(".pdf"):
        try:
            text = scraping.extract_pdf_text(content, max_chars=30000)
        except Exception:
            text = None
    else:
        try:
            text = content.decode("utf-8", errors="replace")[:30000]
        except Exception:
            text = None
    result = await db.execute(
        """update evidence_items set file_path=$3, status='provided',
           ai_notes=coalesce(ai_notes,'') where id=$1 and case_id=$2""",
        uuid.UUID(item_id), case["id"], rel,
    )
    if result.endswith("0"):
        raise HTTPException(404, "Evidence item not found")
    await db.execute(
        """insert into uploads(case_id, kind, filename, file_path, text_extract)
           values($1,'other',$2,$3,$4)""",
        case["id"], file.filename or "evidence", rel, text,
    )
    # Auto-intake: classify, extract facts, date-class — in the background.
    job_id = None
    if text:
        job_id = await jobs.create("evidence_intake", case["id"], {"item": item_id})
        fname = file.filename or "evidence"

        async def work() -> dict:
            return await evidence_intake.process_upload(
                case["id"], uuid.UUID(item_id), fname, text
            )

        background.add_task(jobs.run, job_id, work)
    return {"ok": True, "intake_job_id": job_id}


@router.get("/facts")
async def list_facts(case_id: str, user: dict = Depends(auth.current_user)) -> list[dict]:
    case = await auth.case_owned_by(case_id, user)
    rows = await db.fetch(
        "select category, key, value, as_of, source from case_facts "
        "where case_id=$1 order by category, key", case["id"],
    )
    return [
        {**dict(r), "as_of": r["as_of"].isoformat() if r["as_of"] else None}
        for r in rows
    ]
