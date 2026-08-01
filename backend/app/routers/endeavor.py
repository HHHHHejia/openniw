"""The endeavor composer — the single most important sentence in the case.

Three bounded inputs (method / topic / impact) are mechanically concatenated,
AI-polished into candidates, scored against the six executability elements,
and then FROZEN: every drafted document reuses the sentence verbatim, because
USCIS treats post-filing rewording as a potential material change.
"""
import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from .. import auth, db
from ..services import llm

router = APIRouter(prefix="/api/cases/{case_id}/endeavor", tags=["endeavor"])

SIX_ELEMENTS = [
    "real_world_need", "application_scenario", "implementation_path",
    "beneficiaries", "quantifiable_impact", "means_of_execution",
]

POLISH_SCHEMA = {
    "type": "object",
    "properties": {
        "candidates": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "sentence": {"type": "string"},
                    "pillars": {"type": "array", "items": {"type": "string"}},
                    "rationale": {"type": "string"},
                },
                "required": ["sentence"],
            },
        },
        "element_scores": {
            "type": "object",
            "properties": {k: {"type": "integer", "minimum": 0, "maximum": 2}
                           for k in SIX_ELEMENTS},
        },
        "advice": {"type": "string"},
    },
    "required": ["candidates", "element_scores"],
}


class EndeavorUpdate(BaseModel):
    method: str | None = None
    topic: str | None = None
    impact: str | None = None
    sentence: str | None = None
    pillars: list[str] | None = None
    frozen: bool | None = None


@router.get("")
async def get_endeavor(case_id: str, user: dict = Depends(auth.current_user)) -> dict:
    case = await auth.case_owned_by(case_id, user)
    return case.get("endeavor") or {}


@router.put("")
async def put_endeavor(
    case_id: str, body: EndeavorUpdate, user: dict = Depends(auth.current_user)
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    current = case.get("endeavor") or {}
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    if current.get("frozen") and updates.get("frozen") is not False and (
        set(updates) - {"frozen"}
    ):
        raise HTTPException(
            409,
            "The endeavor is frozen. Unfreeze it explicitly first — rewording "
            "after filing risks a material-change finding.",
        )
    merged = {**current, **updates}
    if all(merged.get(k) for k in ("method", "topic", "impact")) and not updates.get("sentence"):
        merged["composed"] = (
            f"My proposed endeavor is to {merged['method'].strip().rstrip('.')} "
            f"{merged['topic'].strip().rstrip('.')} in order to "
            f"{merged['impact'].strip().rstrip('.')}."
        )
    await db.execute(
        "update cases set endeavor=$2 where id=$1", case["id"], merged
    )
    return merged


@router.post("/polish")
async def polish(case_id: str, user: dict = Depends(auth.current_user)) -> dict:
    case = await auth.case_owned_by(case_id, user)
    endeavor = case.get("endeavor") or {}
    if not any(endeavor.get(k) for k in ("method", "topic", "impact", "sentence", "composed")):
        raise HTTPException(400, "Fill in method/topic/impact first")
    profile = await db.fetchrow("select parsed from profiles where case_id=$1", case["id"])
    messages = await db.fetch(
        "select role, content from messages where case_id=$1 order by created_at desc limit 20",
        case["id"],
    )
    result = await llm.complete(
        "Polish this EB-2 NIW proposed-endeavor draft. Produce 2-3 candidate "
        "canonical sentences of the form 'My proposed endeavor is to [METHOD, "
        "active verbs, at most 3 primary methods] [TOPIC] in order to "
        "[IMPACT].' Each: specific enough to be evidenced, broad enough to "
        "survive a change of employer/project, research-framed, organized "
        "around 2-3 mutually reinforcing pillars (an employer is a deployment "
        "pathway, never a pillar). Then score the SIX executability elements "
        "0-2 based on everything known about the case (0=absent, 1=asserted, "
        "2=evidenced): real_world_need, application_scenario, "
        "implementation_path, beneficiaries, quantifiable_impact, "
        "means_of_execution. means_of_execution (funding/people/entity/"
        "compute/collaborators) is the pass/fail line between 'an executable "
        "project' and 'a personal plan' — be strict. advice: the single most "
        "important improvement.\n\nDRAFT:\n"
        + json.dumps(endeavor, ensure_ascii=False)
        + "\n\nPROFILE:\n"
        + json.dumps(dict(profile["parsed"]) if profile else {}, ensure_ascii=False)[:40000]
        + "\n\nRECENT INTERVIEW:\n"
        + json.dumps([dict(m) for m in messages][::-1], ensure_ascii=False)[:15000],
        schema=POLISH_SCHEMA,
    )
    merged = {**endeavor, "candidates": result.get("candidates"),
              "element_scores": result.get("element_scores"),
              "advice": result.get("advice")}
    await db.execute("update cases set endeavor=$2 where id=$1", case["id"], merged)
    return merged
