"""Citation portfolio review API: a pure file bridge.

The agent writes citations/scored.json (candidate quote cards with its depth
scores); the browser writes citations/selection.json (the user's picks).
Selection is keyed separately from harvest.json so re-harvesting never
clobbers decisions.
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from ..casefolder import CaseFolder, Conflict

router = APIRouter(prefix="/api/citations", tags=["citations"])


def _case(request: Request) -> CaseFolder:
    return request.app.state.case


class SelectionUpdate(BaseModel):
    selection: dict
    base_version: str | int | float | None = None


@router.get("/review")
def review(request: Request) -> dict:
    case = _case(request)
    scored, scored_version = case.read_json(case.scored, default=[])
    selection, version = case.read_json(case.selection)
    return {"scored": scored, "scored_version": scored_version,
            "selection": selection, "version": version}


@router.put("/selection")
def put_selection(request: Request, body: SelectionUpdate) -> dict:
    case = _case(request)
    try:
        version = case.write_json(case.selection, body.selection,
                                  base_version=body.base_version)
    except Conflict as exc:
        raise HTTPException(409, str(exc))
    picked = sum(1 for v in body.selection.values()
                 if isinstance(v, dict) and v.get("selected"))
    case.append_event("saved_selection", picked=picked)
    return {"ok": True, "version": version}
