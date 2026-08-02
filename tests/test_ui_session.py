import os
import time

from openniw import ui_session
from openniw.casefolder import CaseFolder


def _write_running(case, pid=None):
    ui_session.write_sentinel(
        case, step="forms", url="http://127.0.0.1:1/forms/?token=t",
        port=1, pid=pid or os.getpid(), token="t")


def test_none_without_sentinel(tmp_path):
    code, detail = ui_session.status(CaseFolder(tmp_path))
    assert code == ui_session.NONE


def test_live_with_fresh_heartbeat_and_alive_pid(tmp_path):
    case = CaseFolder(tmp_path)
    _write_running(case)
    code, detail = ui_session.status(case)
    assert code == ui_session.LIVE


def test_stale_when_pid_dead(tmp_path):
    case = CaseFolder(tmp_path)
    _write_running(case, pid=99999999)  # nonexistent pid
    code, detail = ui_session.status(case)
    assert code == ui_session.STALE
    assert detail["status"] == "stale"


def test_stale_when_heartbeat_old(tmp_path):
    case = CaseFolder(tmp_path)
    _write_running(case)
    sent = ui_session.read_sentinel(case)
    old = time.strftime("%Y-%m-%dT%H:%M:%S%z",
                        time.localtime(time.time() - 600))
    sent["heartbeat_at"] = old
    case.write_json(case.sentinel, sent)
    code, _ = ui_session.status(case)
    assert code == ui_session.STALE


def test_done_and_abandoned(tmp_path):
    case = CaseFolder(tmp_path)
    _write_running(case)
    ui_session.write_sentinel(
        case, step="forms", url="u", port=1, pid=os.getpid(), token="t",
        status="done", summary={"fields_edited": 3})
    code, detail = ui_session.status(case)
    assert code == ui_session.DONE and detail["summary"]["fields_edited"] == 3

    ui_session.write_sentinel(
        case, step="forms", url="u", port=1, pid=os.getpid(), token="t",
        status="abandoned")
    code, _ = ui_session.status(case)
    assert code == ui_session.ABANDONED


def test_files_owned_recorded(tmp_path):
    case = CaseFolder(tmp_path)
    _write_running(case)
    sent = ui_session.read_sentinel(case)
    assert "forms/answers.json" in sent["files_owned"]
