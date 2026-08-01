import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response
from pydantic import BaseModel

from .. import auth, db
from ..services import docx_export, drafting, jobs

router = APIRouter(prefix="/api/cases/{case_id}/documents", tags=["documents"])

DOC_TITLES = {
    "pes": "Proposed Endeavor Statement",
    "petition_letter": "Petition Letter",
    "reco_letter": "Support Letter",
    "exhibit_list": "Index of Exhibits",
    "cover_letter": "Filing Cover Letter",
    "rfe_response": "RFE Response Plan",
}


class GenerateRequest(BaseModel):
    doc_type: str
    recommender_id: str | None = None
    rfe_text: str | None = None


class ContentUpdate(BaseModel):
    content_md: str
    status: str | None = None


async def _bundle_args(case: dict) -> dict:
    cid = case["id"]
    profile = await db.fetchrow("select * from profiles where case_id=$1", cid)
    ev = await db.fetchrow(
        "select report_md from evaluations where case_id=$1 "
        "order by created_at desc limit 1", cid,
    )
    evidence = [dict(r) for r in await db.fetch(
        "select * from evidence_items where case_id=$1", cid)]
    recommenders = [dict(r) for r in await db.fetch(
        "select * from recommenders where case_id=$1", cid)]
    documents = [dict(r) for r in await db.fetch(
        """select distinct on (doc_type, recommender_id) *
           from documents where case_id=$1
           order by doc_type, recommender_id, version desc""", cid)]
    answers_row = await db.fetchrow(
        "select answers from form_data where case_id=$1", cid)
    messages = await db.fetch(
        "select role, content from messages where case_id=$1 "
        "order by created_at desc limit 40", cid)
    answers = dict(answers_row["answers"]) if answers_row else {}
    answers["_interview_recent"] = [
        {"role": m["role"], "content": m["content"][:2000]} for m in messages
    ][::-1]
    return {
        "case": dict(case),
        "profile": dict(profile["parsed"]) if profile else {},
        "evaluation": {"report_md": ev["report_md"]} if ev else None,
        "evidence": evidence,
        "recommenders": recommenders,
        "documents": documents,
        "answers": answers,
    }


@router.get("")
async def list_documents(
    case_id: str, user: dict = Depends(auth.current_user)
) -> list[dict]:
    case = await auth.case_owned_by(case_id, user)
    rows = await db.fetch(
        """select distinct on (doc_type, recommender_id)
             id, doc_type, recommender_id, version, status, content_md, created_at
           from documents where case_id=$1
           order by doc_type, recommender_id, version desc""",
        case["id"],
    )
    return [
        {
            "id": str(r["id"]),
            "doc_type": r["doc_type"],
            "recommender_id": str(r["recommender_id"]) if r["recommender_id"] else None,
            "version": r["version"],
            "status": r["status"],
            "content_md": r["content_md"],
        }
        for r in rows
    ]


@router.post("/generate")
async def generate(
    case_id: str, body: GenerateRequest, background: BackgroundTasks,
    user: dict = Depends(auth.current_user),
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    if body.doc_type not in DOC_TITLES:
        raise HTTPException(400, f"doc_type must be one of {list(DOC_TITLES)}")
    if body.doc_type == "reco_letter" and not body.recommender_id:
        raise HTTPException(400, "reco_letter requires recommender_id")
    if body.doc_type == "rfe_response" and not body.rfe_text:
        raise HTTPException(400, "rfe_response requires rfe_text")

    job_id = await jobs.create(
        f"draft_{body.doc_type}", case["id"], {"doc_type": body.doc_type}
    )

    async def work() -> dict:
        bundle = await _bundle_args(case)
        if body.doc_type == "reco_letter":
            rec = await db.fetchrow(
                "select * from recommenders where id=$1 and case_id=$2",
                uuid.UUID(body.recommender_id), case["id"],
            )
            if rec is None:
                raise ValueError("Recommender not found")
            content = await drafting.draft_reco_letter(bundle, dict(rec))
            rec_id = rec["id"]
        elif body.doc_type == "rfe_response":
            content = await drafting.draft_rfe_response(bundle, body.rfe_text)
            rec_id = None
        else:
            content = await drafting.DRAFTERS[body.doc_type](bundle)
            rec_id = None
        version = await db.fetchval(
            """select coalesce(max(version),0)+1 from documents
               where case_id=$1 and doc_type=$2
               and recommender_id is not distinct from $3""",
            case["id"], body.doc_type, rec_id,
        )
        doc_id = await db.fetchval(
            """insert into documents
               (case_id, doc_type, recommender_id, version, content_md)
               values($1,$2,$3,$4,$5) returning id""",
            case["id"], body.doc_type, rec_id, version, content,
        )
        return {"document_id": str(doc_id), "version": version}

    background.add_task(jobs.run, job_id, work)
    return {"job_id": job_id}


@router.put("/{document_id}")
async def update_document(
    case_id: str, document_id: str, body: ContentUpdate,
    user: dict = Depends(auth.current_user),
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    result = await db.execute(
        "update documents set content_md=$3, status=coalesce($4,status) "
        "where id=$1 and case_id=$2",
        uuid.UUID(document_id), case["id"], body.content_md, body.status,
    )
    if result.endswith("0"):
        raise HTTPException(404, "Document not found")
    return {"ok": True}


@router.get("/{document_id}/docx")
async def export_docx(
    case_id: str, document_id: str, user: dict = Depends(auth.current_user)
) -> Response:
    case = await auth.case_owned_by(case_id, user)
    row = await db.fetchrow(
        "select * from documents where id=$1 and case_id=$2",
        uuid.UUID(document_id), case["id"],
    )
    if row is None:
        raise HTTPException(404, "Document not found")
    data = docx_export.markdown_to_docx(row["content_md"])
    filename = f"{row['doc_type']}_v{row['version']}.docx"
    return Response(
        content=data,
        media_type=(
            "application/vnd.openxmlformats-officedocument"
            ".wordprocessingml.document"
        ),
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
