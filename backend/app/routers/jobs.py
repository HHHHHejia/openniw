from fastapi import APIRouter, Depends, HTTPException

from .. import auth
from ..services import jobs as jobs_service

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.get("/{job_id}")
async def get_job(job_id: str, user: dict = Depends(auth.current_user)) -> dict:
    job = await jobs_service.get(job_id)
    if job is None:
        raise HTTPException(404, "Job not found")
    return {
        "id": str(job["id"]),
        "kind": job["kind"],
        "status": job["status"],
        "result": job["result"],
        "error": job["error"],
    }


# Public variant used while polling the free evaluation (no account yet).
@router.get("/public/{job_id}")
async def get_public_job(job_id: str) -> dict:
    job = await jobs_service.get(job_id)
    if job is None or job["kind"] != "free_eval":
        raise HTTPException(404, "Job not found")
    return {"id": str(job["id"]), "status": job["status"], "result": job["result"]}
