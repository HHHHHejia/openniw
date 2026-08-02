"""UI-session sentinel: the coordination channel between agent and browser.

One sentinel per case folder (`.openniw/ui-session.json`). The server writes
it (running + heartbeat every 15s, then done/abandoned + summary); the agent
only reads it and deletes it when reconciling a finished session.

Status verdicts (also the CLI exit codes):
    0 live · 2 done · 3 abandoned · 4 stale · 6 none
"""
import json
import os
import time
import urllib.request
from typing import Any

from .casefolder import CaseFolder

HEARTBEAT_SECONDS = 15
STALE_AFTER_SECONDS = 90

FILES_OWNED = {
    "forms": ["forms/answers.json", "forms/answers.meta.json",
              "forms/*-filled.pdf", "forms/fill-report.json"],
    "citations": ["citations/selection.json"],
    "benchmark": ["benchmark.json"],
}

LIVE, DONE, ABANDONED, STALE, NONE = 0, 2, 3, 4, 6


def write_sentinel(case: CaseFolder, *, step: str, url: str, port: int,
                   pid: int, token: str, started_at: str | None = None,
                   status: str = "running", done_at: str | None = None,
                   summary: dict | None = None) -> None:
    case.meta_dir.mkdir(parents=True, exist_ok=True)
    now = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    case.write_json(case.sentinel, {
        "protocol": 1,
        "step": step,
        "status": status,
        "url": url,
        "port": port,
        "pid": pid,
        "token": token,
        "started_at": started_at or now,
        "heartbeat_at": now,
        "done_at": done_at,
        "files_owned": FILES_OWNED.get(step, []),
        "summary": summary,
    })


def read_sentinel(case: CaseFolder) -> dict | None:
    data, version = case.read_json(case.sentinel, default=None)
    return data if version else None


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except (ProcessLookupError, TypeError):
        return False
    except PermissionError:
        return True
    return True


def _healthz_ok(port: int, token: str) -> bool:
    try:
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/api/health",
            headers={"X-OpenNIW-Token": token},
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False


def _heartbeat_age(sent: dict) -> float:
    try:
        hb = time.mktime(time.strptime(sent["heartbeat_at"][:19],
                                       "%Y-%m-%dT%H:%M:%S"))
        return time.time() - hb
    except Exception:
        return float("inf")


def status(case: CaseFolder) -> tuple[int, dict[str, Any]]:
    """Deterministic verdict on the case's UI session.

    Returns (code, detail). Codes: 0 live, 2 done, 3 abandoned, 4 stale,
    6 no sentinel.
    """
    sent = read_sentinel(case)
    if sent is None:
        return NONE, {"status": "none"}
    if sent.get("status") == "done":
        return DONE, sent
    if sent.get("status") == "abandoned":
        return ABANDONED, sent
    # status says running — is it actually alive?
    pid_ok = _pid_alive(int(sent.get("pid") or 0))
    hb_age = _heartbeat_age(sent)
    if not pid_ok or hb_age > STALE_AFTER_SECONDS:
        if _healthz_ok(int(sent.get("port") or 0), sent.get("token") or ""):
            return LIVE, sent  # port responds — trust it over pid/heartbeat
        return STALE, {**sent, "status": "stale",
                       "heartbeat_age_s": round(hb_age, 1),
                       "pid_alive": pid_ok}
    return LIVE, sent


def wait(case: CaseFolder, timeout: float = 540.0,
         poll: float = 2.0) -> tuple[int, dict[str, Any]]:
    """Block until the session leaves the live state or timeout.

    Returns the final status() verdict; on timeout returns (3-style) the
    live verdict with code 5.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        code, detail = status(case)
        if code != LIVE:
            return code, detail
        time.sleep(poll)
    code, detail = status(case)
    return (5, detail) if code == LIVE else (code, detail)
