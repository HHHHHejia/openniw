"""Profile ingestion for an existing case: re-scrape links, absorb uploads
(CV / LinkedIn export), and re-consolidate the structured profile."""

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile

from .. import auth, db
from ..services import evaluation, jobs, scraping, storage

router = APIRouter(prefix="/api/cases/{case_id}/ingest", tags=["ingest"])


@router.post("")
async def ingest(
    case_id: str,
    background: BackgroundTasks,
    scholar_url: str = Form(""),
    homepage_url: str = Form(""),
    linkedin_text: str = Form(""),
    notes: str = Form(""),
    cv: UploadFile | None = File(None),
    linkedin_pdf: UploadFile | None = File(None),
    user: dict = Depends(auth.current_user),
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    cid = case["id"]

    cv_text = None
    if cv is not None:
        content = await cv.read()
        rel = storage.save(str(cid), cv.filename or "cv.pdf", content)
        cv_text = scraping.extract_pdf_text(content) if (
            (cv.filename or "").lower().endswith(".pdf")
        ) else content.decode("utf-8", errors="replace")[:40000]
        await db.execute(
            """insert into uploads(case_id, kind, filename, file_path, text_extract)
               values($1,'cv',$2,$3,$4)""",
            cid, cv.filename or "cv.pdf", rel, cv_text,
        )
    li_text = linkedin_text or None
    if linkedin_pdf is not None:
        content = await linkedin_pdf.read()
        rel = storage.save(str(cid), linkedin_pdf.filename or "linkedin.pdf", content)
        li_text = scraping.extract_pdf_text(content)
        await db.execute(
            """insert into uploads(case_id, kind, filename, file_path, text_extract)
               values($1,'linkedin',$2,$3,$4)""",
            cid, linkedin_pdf.filename or "linkedin.pdf", rel, li_text,
        )

    job_id = await jobs.create("ingest", cid, {})

    async def work() -> dict:
        prev = await db.fetchrow("select * from profiles where case_id=$1", cid)
        basics = {"field": case.get("field")}
        sources = await evaluation.gather_sources(
            scholar_url or (prev["scholar_url"] if prev else None),
            homepage_url or (prev["homepage_url"] if prev else None),
            cv_text, li_text, notes or None,
        )
        if prev and prev["parsed"]:
            sources["previous_profile"] = prev["parsed"]
        profile = await evaluation.consolidate_profile(sources, basics)
        await db.execute(
            """insert into profiles(case_id, scholar_url, homepage_url, raw, parsed)
               values($1,$2,$3,$4,$5)
               on conflict (case_id) do update set
                 scholar_url=coalesce(nullif($2,''), profiles.scholar_url),
                 homepage_url=coalesce(nullif($3,''), profiles.homepage_url),
                 raw=$4, parsed=$5, updated_at=now()""",
            cid, scholar_url, homepage_url,
            {"sources_kept": list(sources.keys())}, profile,
        )
        return {"ok": True}

    background.add_task(jobs.run, job_id, work)
    return {"job_id": job_id}
