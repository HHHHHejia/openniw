"""Forms wizard API over the case folder. No DB, no auth, no LLM."""
import pathlib
import time

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ..casefolder import CaseFolder, Conflict
from ..services import formfill, forms_spec, package_zip

router = APIRouter(prefix="/api/forms", tags=["forms"])


def _case(request: Request) -> CaseFolder:
    return request.app.state.case


class AnswersUpdate(BaseModel):
    answers: dict
    base_version: str | int | float | None = None
    edited_keys: list[str] = []
    verified_keys: list[str] = []


@router.get("/spec")
def spec(request: Request) -> dict:
    case = _case(request)
    answers, _ = case.read_json(case.answers)
    emp = answers.get("current_employer") or {}
    work_state = (emp.get("state") if isinstance(emp, dict) else None) \
        or answers.get("mailing.state")
    return {
        "sections": forms_spec.WIZARD,
        "forms": list(formfill.FORM_SOURCES.keys()),
        "fees": forms_spec.FEES,
        "lockbox_note": forms_spec.LOCKBOX_NOTE,
        "filing_address": forms_spec.filing_address(
            work_state, premium=answers.get("processing.premium") is True
        ),
    }


@router.get("/answers")
def get_answers(request: Request) -> dict:
    case = _case(request)
    answers, version = case.read_json(case.answers)
    meta, _ = case.read_json(case.answers_meta)
    return {"answers": answers, "meta": meta, "version": version}


@router.put("/answers")
def put_answers(request: Request, body: AnswersUpdate) -> dict:
    case = _case(request)
    try:
        version = case.write_json(case.answers, body.answers,
                                  base_version=body.base_version)
    except Conflict as exc:
        raise HTTPException(409, str(exc))
    # editing OR explicitly verifying a field clears its AI-prefill mark;
    # both count as human review and land in meta.verified_keys
    meta, _ = case.read_json(case.answers_meta)
    reviewed = set(body.edited_keys) | set(body.verified_keys)
    if reviewed:
        if meta.get("ai_keys"):
            meta["ai_keys"] = [k for k in meta["ai_keys"]
                               if k not in reviewed]
        if body.edited_keys:
            meta["edited_keys"] = sorted(
                set(meta.get("edited_keys") or []) | set(body.edited_keys))
        meta["verified_keys"] = sorted(
            set(meta.get("verified_keys") or []) | reviewed)
        meta["last_ui_save"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        case.write_json(case.answers_meta, meta)
    case.append_event("saved_answers", edited=len(body.edited_keys),
                      verified=len(body.verified_keys))
    return {"ok": True, "version": version}


@router.post("/fill/{form_code}")
def fill(request: Request, form_code: str) -> dict:
    case = _case(request)
    if form_code not in formfill.FORM_SOURCES:
        raise HTTPException(404, f"unknown form {form_code}")
    answers, _ = case.read_json(case.answers)
    if not answers:
        raise HTTPException(422, "forms/answers.json is empty — nothing to fill")
    try:
        pdf, report = formfill.fill(form_code, answers, case.blank_dir)
    except FileNotFoundError as exc:
        raise HTTPException(422, str(exc))
    out = case.forms_dir / f"{form_code}-filled.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(pdf)
    reports, _ = case.read_json(case.fill_report)
    reports[form_code] = {**report,
                          "at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    case.write_json(case.fill_report, reports)
    case.append_event("filled_form", form=form_code,
                      filled=report["filled"],
                      unmatched=len(report["unmatched_fields"]))
    return {"form_code": form_code, "report": report}


@router.get("/filled")
def filled(request: Request) -> dict:
    case = _case(request)
    out = []
    if case.forms_dir.is_dir():
        for pdf in sorted(case.forms_dir.glob("*-filled.pdf")):
            out.append({"form_code": pdf.name.removesuffix("-filled.pdf"),
                        "mtime": pdf.stat().st_mtime})
    return {"filled": out}


@router.get("/filled/{form_code}/pdf")
def filled_pdf(request: Request, form_code: str) -> FileResponse:
    case = _case(request)
    path = case.forms_dir / f"{pathlib.PurePosixPath(form_code).name}-filled.pdf"
    if not path.exists():
        raise HTTPException(404, "not filled yet")
    return FileResponse(path, media_type="application/pdf",
                        content_disposition_type="inline")


@router.get("/package")
def package(request: Request) -> Response:
    case = _case(request)
    data = package_zip.build_package(case.root)
    out = case.root / "package" / "openniw-package.zip"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    case.append_event("built_package", bytes=len(data))
    return Response(
        content=data, media_type="application/zip",
        headers={"Content-Disposition":
                 'attachment; filename="openniw-package.zip"'},
    )
