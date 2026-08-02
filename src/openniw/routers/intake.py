"""Stage-I intake bridge: links, uploaded source files, and the fixed
background questions — everything standardizable about "getting to know
the applicant" happens in the browser; the agent then does the
non-standard part (fetching, reading, profiling) back in chat."""
import pathlib
import re
import time

from fastapi import APIRouter, HTTPException, Request, UploadFile
from pydantic import BaseModel

from ..casefolder import CaseFolder

router = APIRouter(prefix="/api/intake", tags=["intake"])

MAX_UPLOAD = 50 * 1024 * 1024  # 50 MB per file


def _case(request: Request) -> CaseFolder:
    return request.app.state.case


def _sources(case: CaseFolder) -> pathlib.Path:
    d = case.root / "sources"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _safe_name(name: str) -> str:
    base = pathlib.PurePosixPath(name.replace("\\", "/")).name
    base = re.sub(r"[^\w.\- ()一-鿿]", "_", base).strip() or "upload"
    return base[:120]


def _file_list(case: CaseFolder) -> list[dict]:
    out = []
    d = case.root / "sources"
    if d.is_dir():
        for p in sorted(d.iterdir()):
            if p.is_file() and not p.name.startswith("."):
                out.append({"name": p.name, "size": p.stat().st_size,
                            "mtime": p.stat().st_mtime})
    return out


class IntakeUpdate(BaseModel):
    intake: dict


@router.get("")
def get_intake(request: Request) -> dict:
    case = _case(request)
    intake, version = case.read_json(case.root / "intake.json")
    return {"intake": intake, "version": version, "files": _file_list(case)}


@router.put("")
def put_intake(request: Request, body: IntakeUpdate) -> dict:
    case = _case(request)
    version = case.write_json(case.root / "intake.json", body.intake)
    links = body.intake.get("links") or {}
    case.append_event("saved_intake",
                      links=sum(1 for v in links.values() if v))
    return {"ok": True, "version": version}


@router.post("/upload")
async def upload(request: Request, file: UploadFile) -> dict:
    case = _case(request)
    data = await file.read()
    if len(data) > MAX_UPLOAD:
        raise HTTPException(413, "file larger than 50 MB")
    if not data:
        raise HTTPException(422, "empty file")
    name = _safe_name(file.filename or "upload")
    dest = _sources(case) / name
    if dest.exists():  # never clobber — suffix with a timestamp
        stem, dot, ext = name.rpartition(".")
        name = (f"{stem}-{int(time.time())}.{ext}" if dot
                else f"{name}-{int(time.time())}")
        dest = _sources(case) / name
    dest.write_bytes(data)
    case.append_event("uploaded_source", name=name, bytes=len(data))
    return {"ok": True, "name": name, "files": _file_list(case)}
