"""The source-registry linter must catch the ways a claim table stops
supporting the weight put on it — including the quiet way: cells that look
filled in but say nothing."""
import pathlib

from openniw.services import registry

GOOD = """# Source registry

## Load-bearing claims

| claim | source | locator | independent verifier | measure | gap |
|---|---|---|---|---|---|
| The method was adopted by the X consortium | Ex. 12 | Ex. 12 at 3, ¶2 | Dr. A, consortium chair (no shared work) | 4 member labs | |
| Cited by 41 independent papers | Ex. 14 | Ex. 14 at 1 | Scholar export, third-party | 41 as of 2026-06 | |

## Supporting facts

| claim | source |
|---|---|
| PhD conferred 2023-05 | Ex. 2 |
"""


def _rows(text):
    rows, findings = registry.parse(text)
    return rows, findings


def test_parses_both_tiers():
    rows, findings = _rows(GOOD)
    assert not findings, findings
    assert len(rows) == 3
    assert sum(1 for r in rows if r.tier == registry.LOAD_BEARING) == 2
    assert registry.check(rows) == []


def test_missing_source_is_an_error():
    text = GOOD.replace("| Ex. 12 | Ex. 12 at 3, ¶2 |", "|  | Ex. 12 at 3, ¶2 |")
    rows, _ = _rows(text)
    msgs = [f.message for f in registry.check(rows) if f.severity == "error"]
    assert any("no source" in m for m in msgs), msgs


def test_missing_verifier_is_an_error_only_for_load_bearing():
    text = GOOD.replace("| Dr. A, consortium chair (no shared work) |", "|  |")
    rows, _ = _rows(text)
    errors = [f for f in registry.check(rows) if f.severity == "error"]
    assert len(errors) == 1 and "independent verifier" in errors[0].message
    # the supporting row has no verifier column at all and must stay silent
    assert all("PhD conferred" not in f.claim for f in registry.check(rows))


def test_filler_cells_do_not_count_as_filled():
    for filler in ("-", "N/A", "TBD", "see above", "?", "same as above"):
        text = GOOD.replace("| Dr. A, consortium chair (no shared work) |",
                            f"| {filler} |")
        rows, _ = _rows(text)
        errors = [f for f in registry.check(rows) if f.severity == "error"]
        assert errors and "independent verifier" in errors[0].message, filler


def test_self_serving_is_a_decision_not_an_error():
    text = GOOD.replace("| Dr. A, consortium chair (no shared work) |",
                        "| NONE — self-serving (employer letter) |")
    rows, _ = _rows(text)
    found = registry.check(rows)
    assert [f.severity for f in found] == ["decide"]
    assert "cut the claim" in found[0].message


def test_dead_exhibit_reference_is_caught():
    rows, _ = _rows(GOOD)
    found = registry.check(rows, exhibits={2, 14})   # 12 is missing
    assert any(f.severity == "error" and "not in the exhibit index" in f.message
               for f in found)


def test_duplicate_claim_is_flagged_as_possible_contradiction():
    text = GOOD.replace(
        "| Cited by 41 independent papers | Ex. 14 | Ex. 14 at 1 |",
        "| Cited by 41 independent papers | Ex. 14 | Ex. 14 at 1 |\n"
        "| Cited by 41 independent papers | Ex. 15 | Ex. 15 at 1 |"
        " | Scholar export | 52 as of 2026-07 | |\n| x | y | z | w | v | u |"
        .replace("\n| x | y | z | w | v | u |", ""))
    rows, _ = _rows(text)
    assert any("contradiction" in f.message for f in registry.check(rows))


def test_wrong_header_is_reported():
    text = GOOD.replace("| claim | source | locator | independent verifier |"
                        " measure | gap |",
                        "| claim | source | notes |")
    _, findings = _rows(text)
    assert any("header" in f.message for f in findings)


def test_prose_registry_yields_a_clear_error(tmp_path: pathlib.Path):
    docs = tmp_path / "documents"
    docs.mkdir()
    (docs / "source-registry.md").write_text(
        "# Source registry\n\nEverything is well sourced, trust me.\n")
    report = registry.check_case(tmp_path)
    assert not report["ok"]
    assert any("no claim rows" in f["message"] for f in report["findings"])


def test_missing_file_reports_absence(tmp_path: pathlib.Path):
    report = registry.check_case(tmp_path)
    assert report["exists"] is False and report["ok"] is False


def test_exhibit_cross_check_uses_the_index(tmp_path: pathlib.Path):
    docs = tmp_path / "documents"
    docs.mkdir()
    (docs / "source-registry.md").write_text(GOOD)
    (docs / "exhibit-index.md").write_text(
        "1. CV\n2. Diploma\n12. Consortium letter\n14. Scholar export\n")
    report = registry.check_case(tmp_path)
    assert report["exhibit_index"] is True
    assert report["ok"], report["findings"]
    assert report["rows"] == 3 and report["load_bearing"] == 2
