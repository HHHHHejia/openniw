import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from .. import auth, db

router = APIRouter(prefix="/api/cases/{case_id}/recommenders", tags=["recommenders"])


class RecommenderIn(BaseModel):
    name: str
    title: str | None = None
    org: str | None = None
    relationship: str = "independent"
    angle: str | None = None
    email: str | None = None


@router.get("")
async def list_recommenders(
    case_id: str, user: dict = Depends(auth.current_user)
) -> list[dict]:
    case = await auth.case_owned_by(case_id, user)
    rows = await db.fetch(
        "select * from recommenders where case_id=$1 order by created_at", case["id"]
    )
    return [
        {
            "id": str(r["id"]), "name": r["name"], "title": r["title"],
            "org": r["org"], "relationship": r["relationship"],
            "angle": r["angle"], "email": r["email"], "status": r["status"],
        }
        for r in rows
    ]


@router.post("")
async def add_recommender(
    case_id: str, body: RecommenderIn, user: dict = Depends(auth.current_user)
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    rec_id = await db.fetchval(
        """insert into recommenders(case_id, name, title, org, relationship, angle, email)
           values($1,$2,$3,$4,$5,$6,$7) returning id""",
        case["id"], body.name, body.title, body.org, body.relationship,
        body.angle, body.email,
    )
    return {"id": str(rec_id)}


@router.put("/{rec_id}")
async def update_recommender(
    case_id: str, rec_id: str, body: RecommenderIn,
    user: dict = Depends(auth.current_user),
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    result = await db.execute(
        """update recommenders set name=$3, title=$4, org=$5, relationship=$6,
           angle=$7, email=$8 where id=$1 and case_id=$2""",
        uuid.UUID(rec_id), case["id"], body.name, body.title, body.org,
        body.relationship, body.angle, body.email,
    )
    if result.endswith("0"):
        raise HTTPException(404, "Recommender not found")
    return {"ok": True}


@router.delete("/{rec_id}")
async def delete_recommender(
    case_id: str, rec_id: str, user: dict = Depends(auth.current_user)
) -> dict:
    case = await auth.case_owned_by(case_id, user)
    await db.execute(
        "delete from recommenders where id=$1 and case_id=$2",
        uuid.UUID(rec_id), case["id"],
    )
    return {"ok": True}
