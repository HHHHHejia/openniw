import pytest

from openniw.casefolder import CaseFolder, Conflict


def test_atomic_write_and_version(tmp_path):
    case = CaseFolder(tmp_path)
    v1 = case.write_json(case.answers, {"a": 1})
    data, v = case.read_json(case.answers)
    assert data == {"a": 1} and v == v1 and int(v1) > 0

    v2 = case.write_json(case.answers, {"a": 2}, base_version=v1)
    assert int(v2) >= int(v1)
    with pytest.raises(Conflict):
        case.write_json(case.answers, {"a": 3}, base_version=v1)


def test_missing_file_reads_default(tmp_path):
    case = CaseFolder(tmp_path)
    data, v = case.read_json(case.scored, default=[])
    assert data == [] and v == "0"


def test_events_append(tmp_path):
    case = CaseFolder(tmp_path)
    case.append_event("saved_answers", edited=3)
    case.append_event("done")
    lines = case.events.read_text().strip().splitlines()
    assert len(lines) == 2 and '"saved_answers"' in lines[0]
