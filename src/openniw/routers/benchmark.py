"""Benchmark inputs bridge: the user's self-comparison parameters + computed
percentiles land in benchmark.json for the agent's evaluation calibration.
The dataset itself is static (served with the UI bundle)."""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from ..casefolder import CaseFolder, Conflict

router = APIRouter(prefix="/api/benchmark", tags=["benchmark"])


class InputsUpdate(BaseModel):
    inputs: dict


def _case(request: Request) -> CaseFolder:
    return request.app.state.case


@router.get("/inputs")
def get_inputs(request: Request) -> dict:
    case = _case(request)
    inputs, version = case.read_json(case.root / "benchmark.json")
    return {"inputs": inputs, "version": version}


@router.put("/inputs")
def put_inputs(request: Request, body: InputsUpdate) -> dict:
    case = _case(request)
    try:
        version = case.write_json(case.root / "benchmark.json", body.inputs)
    except Conflict as exc:  # pragma: no cover — no base_version used here
        raise HTTPException(409, str(exc))
    case.append_event("saved_benchmark",
                      percentile=(body.inputs.get("computed") or {})
                      .get("percentile_among_approved"))
    return {"ok": True, "version": version}
