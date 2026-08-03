"""Regression: optimistic-concurrency versions must survive a JavaScript
round-trip. mtime_ns (~1.8e18) exceeds Number.MAX_SAFE_INTEGER (~9e15), so
browsers round it — versions are now strings, and rounded numeric values
from pre-fix tabs are accepted within double-precision tolerance."""
import json
import struct

from openniw.casefolder import CaseFolder, Conflict
import pytest


def js_roundtrip(n: int) -> float:
    """What a browser's JSON.parse does to a big integer: IEEE-754 double."""
    return struct.unpack("d", struct.pack("d", float(n)))[0]


def test_version_is_string(tmp_path):
    case = CaseFolder(tmp_path)
    v = case.write_json(case.answers, {"a": 1})
    assert isinstance(v, str) and int(v) > 10**17
    _, v2 = case.read_json(case.answers)
    assert isinstance(v2, str)


def test_string_version_roundtrip_exact(tmp_path):
    case = CaseFolder(tmp_path)
    v = case.write_json(case.answers, {"a": 1})
    case.write_json(case.answers, {"a": 2}, base_version=v)  # no Conflict


def test_js_rounded_numeric_version_accepted(tmp_path):
    """A pre-fix browser tab holds round(mtime_ns) as a double — its save
    must still be accepted (this exact scenario ate a user's form data)."""
    case = CaseFolder(tmp_path)
    v = int(case.write_json(case.answers, {"a": 1}))
    rounded = js_roundtrip(v)
    assert rounded != v or (v % 4096 == 0)  # doubles can't hold this exactly
    case.write_json(case.answers, {"a": 2}, base_version=rounded)  # accepted


def test_actually_stale_numeric_version_still_conflicts(tmp_path):
    case = CaseFolder(tmp_path)
    v1 = int(case.write_json(case.answers, {"a": 1}))
    import time
    time.sleep(0.01)
    case.write_json(case.answers, {"a": 2})  # someone else wrote
    with pytest.raises(Conflict):
        case.write_json(case.answers, {"a": 3}, base_version=js_roundtrip(v1))


def test_api_version_serializes_as_string(client):
    got = client.get("/api/forms/answers").json()
    assert isinstance(got["version"], str)
    # and the exact string round-trips through a save
    ok = client.put("/api/forms/answers", json={
        "answers": got["answers"], "base_version": got["version"],
        "edited_keys": []})
    assert ok.status_code == 200
    assert isinstance(ok.json()["version"], str)


def test_api_accepts_js_rounded_number(client):
    got = client.get("/api/forms/answers").json()
    rounded = js_roundtrip(int(got["version"]))
    ok = client.put("/api/forms/answers", json={
        "answers": got["answers"], "base_version": rounded,
        "edited_keys": []})
    assert ok.status_code == 200


def test_cli_refuses_project_root_launch(tmp_path):
    from openniw.cli import _check_case_dir
    from openniw.casefolder import CaseFolder as CF
    (tmp_path / "niw-case").mkdir()
    (tmp_path / "niw-case" / "STATE.md").write_text("# Case state")
    msg = _check_case_dir(CF(tmp_path))
    assert msg and "niw-case" in msg
    assert _check_case_dir(CF(tmp_path / "niw-case")) is None
    # brand-new empty dir is allowed (agent creates STATE.md right after)
    empty = tmp_path / "fresh"
    empty.mkdir()
    assert _check_case_dir(CF(empty)) is None
