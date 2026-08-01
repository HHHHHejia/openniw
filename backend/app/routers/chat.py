"""The AI intake interview — replaces the traditional questionnaire.

Asks only for what automated ingestion could not derive.
"""
import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .. import auth, db, prompts
from ..services import llm

router = APIRouter(prefix="/api/cases/{case_id}/chat", tags=["chat"])


class MessageIn(BaseModel):
    content: str


@router.get("")
async def history(case_id: str, user: dict = Depends(auth.current_user)) -> list[dict]:
    case = await auth.case_owned_by(case_id, user)
    rows = await db.fetch(
        "select role, content, created_at from messages where case_id=$1 "
        "order by created_at", case["id"],
    )
    return [
        {"role": r["role"], "content": r["content"],
         "created_at": r["created_at"].isoformat()}
        for r in rows
    ]


@router.post("")
async def send(
    case_id: str, body: MessageIn, user: dict = Depends(auth.current_user)
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    cid = case["id"]
    await db.execute(
        "insert into messages(case_id, role, content) values($1,'user',$2)",
        cid, body.content,
    )
    profile = await db.fetchrow("select parsed from profiles where case_id=$1", cid)
    ev = await db.fetchrow(
        "select report_md from evaluations where case_id=$1 "
        "order by created_at desc limit 1", cid,
    )
    evidence = await db.fetch(
        "select category, title, status from evidence_items where case_id=$1", cid
    )
    history_rows = await db.fetch(
        "select role, content from messages where case_id=$1 "
        "order by created_at desc limit 30", cid,
    )
    context = {
        "profile": dict(profile["parsed"]) if profile else {},
        "evaluation_excerpt": (ev["report_md"] or "")[:8000] if ev else "",
        "checklist": [dict(r) for r in evidence],
    }
    convo = "\n".join(
        f"{r['role'].upper()}: {r['content']}" for r in reversed(history_rows)
    )
    reply = await llm.complete(
        "CASE CONTEXT:\n" + json.dumps(context, ensure_ascii=False)[:60000]
        + "\n\nCONVERSATION SO FAR:\n" + convo[-20000:]
        + "\n\nRespond as the intake assistant (continue the conversation).",
        system=prompts.load("interview"),
        effort="medium",
    )
    await db.execute(
        "insert into messages(case_id, role, content) values($1,'assistant',$2)",
        cid, reply,
    )
    return {"reply": reply}
