"""Public free-evaluation endpoint — the top of the funnel.

The user gives links (Scholar/homepage) and/or pastes CV/LinkedIn text; we do
the rest. No account required; the result id is an unguessable UUID.
"""
import json
import uuid

from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from .. import db, prompts
from ..services import evaluation, jobs, llm, scraping

router = APIRouter(prefix="/api/eval", tags=["eval"])


def _sse(event: dict) -> str:
    return f"data: {json.dumps(event, ensure_ascii=False)}\n\n"


@router.post("/free")
async def free_eval(
    background: BackgroundTasks,
    email: str = Form(...),
    field: str = Form(""),
    highest_degree: str = Form(""),
    visa_status: str = Form(""),
    scholar_url: str = Form(""),
    homepage_url: str = Form(""),
    linkedin_text: str = Form(""),
    notes: str = Form(""),
    defer: str = Form(""),
    cv: UploadFile | None = File(None),
) -> dict:
    if not (scholar_url or homepage_url or linkedin_text or cv or notes):
        raise HTTPException(
            400,
            "Provide at least one source: Scholar URL, homepage, LinkedIn text, or CV",
        )
    cv_text = None
    if cv is not None:
        content = await cv.read()
        if cv.filename and cv.filename.lower().endswith(".pdf"):
            cv_text = scraping.extract_pdf_text(content)
        else:
            cv_text = content.decode("utf-8", errors="replace")[:40000]

    basics = {
        "email": email,
        "field": field,
        "highest_degree": highest_degree,
        "visa_status": visa_status,
    }
    if defer == "true":
        # Streaming mode: store the inputs; /{id}/stream runs the pipeline.
        eval_id = await db.fetchval(
            "insert into evaluations(email, input_snapshot) values($1,$2) returning id",
            email,
            {"basics": basics,
             "deferred_inputs": {
                 "scholar_url": scholar_url, "homepage_url": homepage_url,
                 "linkedin_text": linkedin_text, "cv_text": cv_text,
                 "notes": notes,
             }},
        )
        return {"evaluation_id": str(eval_id), "stream": True}

    eval_id = await db.fetchval(
        "insert into evaluations(email, input_snapshot) values($1,$2) returning id",
        email, {"basics": basics, "scholar_url": scholar_url,
                "homepage_url": homepage_url},
    )
    job_id = await jobs.create("free_eval", None, {"evaluation_id": str(eval_id)})

    async def work() -> dict:
        sources = await evaluation.gather_sources(
            scholar_url or None, homepage_url or None, cv_text,
            linkedin_text or None, notes or None,
        )
        profile = await evaluation.consolidate_profile(sources, basics)
        result = await evaluation.evaluate(profile, basics)
        await db.execute(
            """update evaluations set input_snapshot=$2, report_md=$3, tier=$4,
               prong_scores=$5 where id=$1""",
            eval_id,
            {"basics": basics, "sources_kept": list(sources.keys()),
             "profile": profile},
            result["report_md"], result["tier"], result["prong_scores"],
        )
        return {"evaluation_id": str(eval_id), "tier": result["tier"]}

    background.add_task(jobs.run, job_id, work)
    return {"job_id": job_id, "evaluation_id": str(eval_id)}


@router.get("/{evaluation_id}/stream")
async def stream_eval(evaluation_id: str) -> StreamingResponse:
    """SSE: run (or replay) the evaluation, streaming stages and report text."""
    try:
        eid = uuid.UUID(evaluation_id)
    except ValueError:
        raise HTTPException(404, "Not found")
    row = await db.fetchrow("select * from evaluations where id = $1", eid)
    if row is None:
        raise HTTPException(404, "Not found")

    async def gen():
        if row["report_md"]:  # already evaluated — replay instantly
            yield _sse({"stage": "done", "report_md": row["report_md"],
                        "tier": row["tier"], "prong_scores": row["prong_scores"]})
            return
        snapshot = row["input_snapshot"] or {}
        basics = snapshot.get("basics") or {}
        inputs = snapshot.get("deferred_inputs") or {}
        try:
            yield _sse({"stage": "fetching",
                        "note": "Fetching your public record"})
            sources = await evaluation.gather_sources(
                inputs.get("scholar_url") or None,
                inputs.get("homepage_url") or None,
                inputs.get("cv_text") or None,
                inputs.get("linkedin_text") or None,
                inputs.get("notes") or None,
            )
            yield _sse({"stage": "profiling",
                        "note": "Consolidating your profile",
                        "sources": [k for k in sources if not k.startswith("_")]})
            profile = await evaluation.consolidate_profile(sources, basics)
            yield _sse({"stage": "evaluating",
                        "note": "Applying the Dhanasar framework"})
            report_parts: list[str] = []
            async for delta in llm.stream(
                evaluation.eval_prompt(profile, basics),
                system=prompts.load("evaluation"),
            ):
                report_parts.append(delta)
                yield _sse({"delta": delta})
            report_md = "".join(report_parts)
            scored = await evaluation.extract_tier(report_md)
            await db.execute(
                """update evaluations set input_snapshot=$2, report_md=$3,
                   tier=$4, prong_scores=$5 where id=$1""",
                eid,
                {"basics": basics, "sources_kept": list(sources.keys()),
                 "profile": profile},
                report_md, scored.get("tier", "borderline"),
                scored.get("prong_scores", {}),
            )
            yield _sse({"stage": "done", "tier": scored.get("tier"),
                        "prong_scores": scored.get("prong_scores", {})})
        except Exception as exc:
            yield _sse({"stage": "error", "error": str(exc)[:500]})

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/{evaluation_id}")
async def get_eval(evaluation_id: str) -> dict:
    try:
        eid = uuid.UUID(evaluation_id)
    except ValueError:
        raise HTTPException(404, "Not found")
    row = await db.fetchrow("select * from evaluations where id = $1", eid)
    if row is None:
        raise HTTPException(404, "Not found")
    return {
        "id": str(row["id"]),
        "status": "done" if row["report_md"] else "pending",
        "tier": row["tier"],
        "prong_scores": row["prong_scores"],
        "report_md": row["report_md"],
        "created_at": row["created_at"].isoformat(),
    }
