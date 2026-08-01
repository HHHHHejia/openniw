import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from .. import auth, db
from ..services import citations, jobs

router = APIRouter(prefix="/api/cases/{case_id}/citations", tags=["citations"])


class StatusUpdate(BaseModel):
    status: str  # selected | rejected | scored
    reject_reason: str | None = None


async def _surname(case_id) -> str:
    profile = await db.fetchrow("select parsed from profiles where case_id=$1", case_id)
    name = ((profile or {}).get("parsed") or {}).get("name") if profile else None
    answers = await db.fetchrow("select answers from form_data where case_id=$1", case_id)
    if answers and answers["answers"].get("beneficiary.family_name"):
        return answers["answers"]["beneficiary.family_name"]
    if name:
        return name.split()[-1]
    return ""


@router.get("/summary")
async def summary(case_id: str, user: dict = Depends(auth.current_user)) -> dict:
    case = await auth.case_owned_by(case_id, user)
    row = await db.fetchrow(
        """select count(*) total,
                  count(*) filter (where independent) independent,
                  count(*) filter (where independent and published) usable_pool,
                  count(*) filter (where verified_in_text) verified,
                  count(*) filter (where verified_in_text is false) false_positives,
                  count(*) filter (where negative) negative,
                  count(*) filter (where same_surname_flag) needs_review,
                  count(*) filter (where status='selected') selected
           from citing_papers where case_id=$1""",
        case["id"],
    )
    pct = None
    if row and row["total"]:
        pct = round(100 * row["independent"] / row["total"], 1)
    return {**(dict(row) if row else {}), "independent_pct": pct}


@router.get("")
async def list_citations(
    case_id: str, status: str | None = None,
    user: dict = Depends(auth.current_user),
) -> list[dict]:
    case = await auth.case_owned_by(case_id, user)
    query = "select * from citing_papers where case_id=$1"
    args: list = [case["id"]]
    if status:
        query += " and status=$2"
        args.append(status)
    query += " order by score desc nulls last, citing_year desc nulls last limit 400"
    rows = await db.fetch(query, *args)
    return [
        {
            "id": str(r["id"]),
            "cited_title": r["cited_title"],
            "citing_title": r["citing_title"],
            "citing_venue": r["citing_venue"],
            "citing_year": r["citing_year"],
            "citing_authors": r["citing_authors"],
            "published": r["published"],
            "independent": r["independent"],
            "same_surname_flag": r["same_surname_flag"],
            "verified_in_text": r["verified_in_text"],
            "use_type": r["use_type"],
            "score": r["score"],
            "negative": r["negative"],
            "status": r["status"],
            "reject_reason": r["reject_reason"],
            "quote_context": r["quote_context"],
            "has_pdf": r["pdf_path"] is not None,
        }
        for r in rows
    ]


@router.post("/harvest")
async def start_harvest(
    case_id: str, background: BackgroundTasks, user: dict = Depends(auth.current_user)
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    profile = await db.fetchrow("select parsed from profiles where case_id=$1", case["id"])
    pubs = ((profile["parsed"] if profile else {}) or {}).get("publications") or []
    titles = [p.get("title") for p in pubs if p.get("title")]
    if not titles:
        raise HTTPException(400, "No publications in the profile — run source analysis first")
    job_id = await jobs.create("citations_harvest", case["id"], {"titles": len(titles)})

    async def work() -> dict:
        return await citations.harvest(case["id"], titles)

    background.add_task(jobs.run, job_id, work)
    return {"job_id": job_id}


@router.post("/verify")
async def start_verify(
    case_id: str, background: BackgroundTasks, user: dict = Depends(auth.current_user)
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    surname = await _surname(case["id"])
    if not surname:
        raise HTTPException(400, "Applicant name unknown — analyze sources or fill the forms wizard first")
    job_id = await jobs.create("citations_verify", case["id"], {})

    async def work() -> dict:
        result = await citations.run_verification(case["id"], surname)
        result.update(await citations.select_portfolio(case["id"]))
        return result

    background.add_task(jobs.run, job_id, work)
    return {"job_id": job_id}


@router.post("/deliverables")
async def build_deliverables(
    case_id: str, background: BackgroundTasks, user: dict = Depends(auth.current_user)
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    surname = await _surname(case["id"])
    job_id = await jobs.create("citations_deliverables", case["id"], {})

    async def work() -> dict:
        return await citations.build_deliverables(case["id"], surname)

    background.add_task(jobs.run, job_id, work)
    return {"job_id": job_id}


@router.put("/{citation_id}/status")
async def set_status(
    case_id: str, citation_id: str, body: StatusUpdate,
    user: dict = Depends(auth.current_user),
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    if body.status not in ("selected", "rejected", "scored"):
        raise HTTPException(400, "status must be selected/rejected/scored")
    result = await db.execute(
        """update citing_papers set status=$3, reject_reason=$4
           where id=$1 and case_id=$2""",
        uuid.UUID(citation_id), case["id"], body.status, body.reject_reason,
    )
    if result.endswith("0"):
        raise HTTPException(404, "Citation not found")
    return {"ok": True}


@router.get("/recommender-candidates")
async def candidates(case_id: str, user: dict = Depends(auth.current_user)) -> list[dict]:
    case = await auth.case_owned_by(case_id, user)
    return await citations.recommender_candidates(case["id"])
