import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from .. import auth, db
from ..services import checklist, jobs

router = APIRouter(prefix="/api/cases", tags=["cases"])

STAGES = ["eval", "collect", "draft", "forms", "package", "rfe"]


class CaseCreate(BaseModel):
    title: str = "My NIW Case"
    field: str | None = None
    evaluation_id: str | None = None  # link a completed free evaluation


class StageUpdate(BaseModel):
    stage: str


@router.get("")
async def list_cases(user: dict = Depends(auth.current_user)) -> list[dict]:
    rows = await db.fetch(
        "select id, title, field, stage, created_at from cases "
        "where user_id=$1 order by created_at desc",
        user["id"],
    )
    return [
        {**dict(r), "id": str(r["id"]), "created_at": r["created_at"].isoformat()}
        for r in rows
    ]


@router.post("")
async def create_case(
    body: CaseCreate,
    background: BackgroundTasks,
    user: dict = Depends(auth.current_user),
) -> dict:
    case_id = await db.fetchval(
        "insert into cases(user_id, title, field) values($1,$2,$3) returning id",
        user["id"], body.title, body.field,
    )
    profile: dict = {}
    if body.evaluation_id:
        ev = await db.fetchrow(
            "select * from evaluations where id=$1", uuid.UUID(body.evaluation_id)
        )
        if ev is not None:
            await db.execute(
                "update evaluations set case_id=$2 where id=$1", ev["id"], case_id
            )
            snapshot = ev["input_snapshot"] or {}
            profile = snapshot.get("profile") or {}
            await db.execute(
                "insert into profiles(case_id, parsed, raw) values($1,$2,$3)",
                case_id, profile, snapshot,
            )
            # Personalized checklist seeded in the background from the eval.
            job_id = await jobs.create("checklist", case_id, {})

            async def work() -> dict:
                items = await checklist.personalize(profile, ev["report_md"] or "")
                for it in items:
                    await db.execute(
                        """insert into evidence_items
                           (case_id, category, title, description, status, ai_notes)
                           values($1,$2,$3,$4,$5,$6)""",
                        case_id, it.get("category", "other"), it.get("title", ""),
                        it.get("description"),
                        it.get("status", "suggested"), it.get("ai_notes"),
                    )
                return {"items": len(items)}

            background.add_task(jobs.run, job_id, work)
    if not profile:
        await db.execute("insert into profiles(case_id) values($1)", case_id)
        for it in checklist.base_items():
            await db.execute(
                """insert into evidence_items
                   (case_id, category, title, description, status, ai_notes)
                   values($1,$2,$3,$4,'suggested',$5)""",
                case_id, it["category"], it["title"], it["description"],
                it["ai_notes"],
            )
    await db.execute(
        "update cases set stage='collect' where id=$1", case_id
    )
    return {"id": str(case_id)}


@router.get("/{case_id}")
async def get_case(case_id: str, user: dict = Depends(auth.current_user)) -> dict:
    case = await auth.case_owned_by(case_id, user)
    cid = case["id"]
    profile = await db.fetchrow("select * from profiles where case_id=$1", cid)
    ev = await db.fetchrow(
        "select id, tier, prong_scores, report_md, created_at from evaluations "
        "where case_id=$1 order by created_at desc limit 1",
        cid,
    )
    counts = await db.fetchrow(
        """select
             (select count(*) from evidence_items where case_id=$1) as evidence_total,
             (select count(*) from evidence_items where case_id=$1
                and status='provided') as evidence_provided,
             (select count(*) from documents where case_id=$1) as documents,
             (select count(*) from recommenders where case_id=$1) as recommenders,
             (select count(*) from filled_forms where case_id=$1) as filled_forms""",
        cid,
    )
    return {
        "id": str(cid),
        "title": case["title"],
        "field": case["field"],
        "stage": case["stage"],
        "profile": {
            "parsed": profile["parsed"] if profile else {},
            "scholar_url": profile["scholar_url"] if profile else None,
            "homepage_url": profile["homepage_url"] if profile else None,
        },
        "evaluation": None if ev is None else {
            "id": str(ev["id"]),
            "tier": ev["tier"],
            "prong_scores": ev["prong_scores"],
            "report_md": ev["report_md"],
        },
        "counts": dict(counts) if counts else {},
    }


@router.put("/{case_id}/stage")
async def set_stage(
    case_id: str, body: StageUpdate, user: dict = Depends(auth.current_user)
) -> dict:
    if body.stage not in STAGES:
        raise HTTPException(400, f"stage must be one of {STAGES}")
    case = await auth.case_owned_by(case_id, user)
    await db.execute("update cases set stage=$2 where id=$1", case["id"], body.stage)
    return {"ok": True}
