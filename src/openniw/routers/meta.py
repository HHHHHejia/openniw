"""Session/meta API: health, state rendering, and the done handshake."""
import threading
import time

from fastapi import APIRouter, Request
from pydantic import BaseModel

from .. import __version__, ui_session
from ..casefolder import CaseFolder

router = APIRouter(prefix="/api", tags=["meta"])


def _case(request: Request) -> CaseFolder:
    return request.app.state.case


@router.get("/health")
def health(request: Request) -> dict:
    return {"ok": True, "version": __version__,
            "case_dir": str(_case(request).root),
            "step": request.app.state.step}


@router.get("/state")
def state(request: Request) -> dict:
    case = _case(request)
    try:
        state_md = case.state_md.read_text()
    except FileNotFoundError:
        state_md = ""
    case_json, _ = case.read_json(case.case_json)
    return {"state_md": state_md, "case": case_json}


class Finish(BaseModel):
    summary: dict = {}


def _finalize(request: Request, status: str, summary: dict) -> dict:
    app = request.app
    case: CaseFolder = app.state.case
    reports, _ = case.read_json(case.fill_report)
    meta, _ = case.read_json(case.answers_meta)
    full_summary = {
        **summary,
        "fill_reports": {k: {kk: vv for kk, vv in v.items() if kk != "at"}
                         for k, v in reports.items()},
        "ai_keys_remaining": meta.get("ai_keys") or [],
    }
    ui_session.write_sentinel(
        case, step=app.state.step, url=app.state.url, port=app.state.port,
        pid=app.state.pid, token=app.state.token,
        started_at=app.state.started_at, status=status,
        done_at=time.strftime("%Y-%m-%dT%H:%M:%S%z"), summary=full_summary,
    )
    case.append_event(status, step=app.state.step)
    stopper = getattr(app.state, "stop", None)
    if stopper is not None:
        threading.Timer(1.0, stopper).start()
    return {"ok": True, "status": status}


@router.post("/done")
def done(request: Request, body: Finish) -> dict:
    return _finalize(request, "done", body.summary)


@router.post("/later")
def later(request: Request, body: Finish) -> dict:
    return _finalize(request, "abandoned", body.summary)


@router.post("/shutdown")
def shutdown(request: Request) -> dict:
    stopper = getattr(request.app.state, "stop", None)
    if stopper is not None:
        threading.Timer(0.5, stopper).start()
    return {"ok": True}
