"""The 61-key answers contract must stay in sync across three artifacts:
formfill.py (what the PDFs consume), forms_spec.WIZARD (what the UI edits),
and the skill's references/forms.md (what the agent writes)."""
import pathlib
import re

from openniw.services import forms_spec, formfill

REPO = pathlib.Path(__file__).resolve().parents[1]
FORMS_MD = REPO / ".agents" / "skills" / "niw-petition" / "references" / "forms.md"

# Structured (non-scalar) wizard fields expand to nested objects, not flat keys
STRUCTURED = {"degrees", "current_employer", "family"}


def _formfill_keys() -> set[str]:
    src = (REPO / "src" / "openniw" / "services" / "formfill.py").read_text()
    keys = set(re.findall(r'a\.get\("([a-z_]+\.[a-z_0-9]+)"', src))
    return keys


def _wizard_keys() -> set[str]:
    return {f["key"] for s in forms_spec.WIZARD for f in s["fields"]
            if f["key"] not in STRUCTURED}


def _forms_md_keys() -> set[str]:
    text = FORMS_MD.read_text()
    m = re.search(r"## answers\.json key reference.*?## ", text, re.S)
    block = m.group(0) if m else text
    keys: set[str] = set()
    for group_match in re.finditer(
            r"`([a-z_]+)\.\*`[^\n]*:\s*\(?([^`]*?)(?=\n-|\n\n|$)", block, re.S):
        group = group_match.group(1)
        body = group_match.group(2)
        for name in re.findall(r"([a-z_0-9]+)", body):
            if name in {"bool", "default", "true", "e", "g", "etc"}:
                continue
            keys.add(f"{group}.{name}")
    return keys


def test_wizard_covered_by_formfill_or_meta():
    ff = _formfill_keys()
    wiz = _wizard_keys()
    # Every wizard scalar key is either consumed by a PDF builder or is a
    # deliberate non-PDF key (premium drives address/package only).
    non_pdf = {"processing.premium"}
    missing = wiz - ff - non_pdf
    assert not missing, f"wizard keys no PDF consumes: {sorted(missing)}"


def test_formfill_covered_by_wizard():
    ff = _formfill_keys()
    wiz = _wizard_keys()
    missing = ff - wiz
    assert not missing, f"formfill reads keys the wizard cannot edit: {sorted(missing)}"


def test_forms_md_documents_all_formfill_scalars():
    ff = _formfill_keys()
    documented = _forms_md_keys()
    missing = ff - documented
    assert not missing, f"formfill keys undocumented in forms.md: {sorted(missing)}"


def test_wizard_field_count():
    total = sum(len(s["fields"]) for s in forms_spec.WIZARD)
    assert total == 62


def test_filing_address_routing():
    assert forms_spec.filing_address("NY")["key"] == "chicago"
    assert forms_spec.filing_address("TX")["key"] == "dallas"
    assert forms_spec.filing_address("NY", premium=True)["key"] == "elgin_premium"
    assert forms_spec.filing_address("CA", premium=True)["key"] == "phoenix_premium"
    assert forms_spec.filing_address("TX", concurrent_i485=True)["key"] == "dallas_nfb"
