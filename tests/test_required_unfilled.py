"""The Final Determination page carries PDF-flagged Required fields in its
signature blocks. We fill what a self-petitioner can type (names, Title);
everything left blank must be surfaced with an explicit action instead of
shipping silent blanks."""
import pathlib

import pytest

from openniw.services import formfill

REPO = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture
def fd_report(case_dir):
    if not (case_dir / "forms" / "blank"
            / "ETA-9089-Final-Determination.pdf").exists():
        pytest.skip("vendored FD pdf missing")
    import json
    answers = json.loads((case_dir / "forms" / "answers.json").read_text())
    pdf, report = formfill.fill("eta-9089-final-determination", answers,
                                case_dir / "forms" / "blank")
    return pdf, report


def test_petitioner_declaration_block_filled(fd_report):
    pdf, report = fd_report
    import io
    from pypdf import PdfReader
    fields = PdfReader(io.BytesIO(pdf)).get_fields()
    by_suffix = {k.split(".")[-1]: (v.get("/V") or "") for k, v in fields.items()}
    assert by_suffix["1 Last family Name"] == "Doe"
    assert by_suffix["2 First given Name_2"] == "Jane"
    assert by_suffix["4 Title"] == "Self-petitioner"


def test_required_unfilled_categorized(fd_report):
    _, report = fd_report
    ru = report["required_unfilled"]
    actions = {q["field"]: q["action"] for q in ru}
    assert any("Signature" in f and "sign by hand" in a
               for f, a in actions.items())
    assert any("Date Signed" in f and "when you sign" in a
               for f, a in actions.items())
    assert any("Attorney" in f and "attorney" in a
               for f, a in actions.items())
    # nothing typeable-by-us may remain in the list
    assert not any(a == "complete in the wizard or by hand"
                   for a in actions.values()), actions


def test_i140_has_no_required_flags(case_dir):
    import json
    if not (case_dir / "forms" / "blank" / "i-140.pdf").exists():
        pytest.skip("vendored i-140 missing")
    answers = json.loads((case_dir / "forms" / "answers.json").read_text())
    _, report = formfill.fill("i-140", answers, case_dir / "forms" / "blank")
    assert report["required_unfilled"] == []
