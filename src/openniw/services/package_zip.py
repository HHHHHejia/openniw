"""Filing-package ZIP assembly over a case folder.

Contents: filled form PDFs + every markdown document rendered to DOCX +
an assembly README with the USCIS-recommended order and the computed
lockbox mailing address.
"""
import io
import json
import pathlib
import zipfile

from . import docx_export, forms_spec


def _answers(case_dir: pathlib.Path) -> dict:
    p = case_dir / "forms" / "answers.json"
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            return {}
    return {}


def build_readme(answers: dict) -> str:
    premium = answers.get("processing.premium") is True
    emp = answers.get("current_employer") or {}
    work_state = (emp.get("state") if isinstance(emp, dict) else None) \
        or answers.get("mailing.state")
    addr = forms_spec.filing_address(work_state, premium=premium)
    fee_line = (
        f"I-140 fee ${forms_spec.FEES['i-140']} + Asylum Program Fee "
        f"${forms_spec.FEES['asylum_program_fee_self']} (self-petitioner)"
    )
    if premium:
        fee_line += (
            f"; I-907 premium fee ${forms_spec.FEES['i-907_premium']} on "
            "its OWN payment form (one payment per form)"
        )
    items = [
        "Fee payment: G-1650 (ACH, recommended) or G-1450 (credit card; "
        "a declined card rejects the whole package) — " + fee_line,
        "G-1145 e-notification",
        *(["Form I-907 premium processing request (signed)"] if premium
          else []),
        "Cover letter, marked 'Original Submission — Form I-140' (mark "
        "the envelope the same way)",
        "Form I-140 (signed in black ink)",
        "ETA-9089 Appendix A + signed Final Determination (as a "
        "self-petitioner you sign BOTH the petitioner and the "
        "beneficiary blocks; wet signatures)",
        "Foreign name & address page — your name and foreign address in "
        "your native alphabet (only if it is non-Roman; not needed if "
        "born in India)",
        "Identity documents: passport pages with stamps (no blank "
        "pages), current status approval notice, I-94 front and back",
        "Petition Letter",
        "Proposed Endeavor Statement (signed)",
        "Support letters (signed, on letterhead) — put each "
        "recommender's CV (max 5 pages) or a printed bio page behind "
        "their letter",
        "Exhibits in the order of the Index of Exhibits (publications: "
        "first 3-5 pages of each paper are enough; highlight your name "
        "in the author list)",
    ]
    order = "\n".join(f"{i}. {t}" for i, t in enumerate(items, 1))
    return (
        "OPENNIW FILING PACKAGE\n======================\n\n"
        "Assembly order (top to bottom — USCIS-recommended: payment "
        "form first):\n"
        + order + "\n\n"
        f"MAIL TO — {addr['name']}:\n"
        f"USPS:\n{addr['usps']}\n\n"
        f"FedEx/UPS/DHL:\n{addr['courier']}\n"
        f"({addr['note']})\n"
        "If you file I-485 concurrently in the same envelope (no "
        "premium), the address differs: Dallas Lockbox, Attn: NFB.\n\n"
        + forms_spec.LOCKBOX_NOTE
        + "\n\nAny document in a foreign language needs a full English "
        "translation plus the translator's signed certification that "
        "the translation is complete and accurate and that they are "
        "competent to translate. Keep a complete copy of the package. "
        "This package was prepared with OpenNIW, an open-source "
        "document preparation tool. It is not legal advice; review "
        "everything before filing.\n"
    )


def build_package(case_dir: pathlib.Path) -> bytes:
    """Assemble the package ZIP from the case folder; returns ZIP bytes."""
    case_dir = pathlib.Path(case_dir)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        forms_dir = case_dir / "forms"
        if forms_dir.is_dir():
            for pdf in sorted(forms_dir.glob("*-filled.pdf")):
                zf.writestr(f"forms/{pdf.name}", pdf.read_bytes())
        docs_dir = case_dir / "documents"
        if docs_dir.is_dir():
            for md in sorted(docs_dir.rglob("*.md")):
                rel = md.relative_to(docs_dir).with_suffix(".docx")
                try:
                    zf.writestr(f"documents/{rel.as_posix()}",
                                docx_export.markdown_to_docx(md.read_text()))
                except Exception:
                    continue
        zf.writestr("README.txt", build_readme(_answers(case_dir)))
    return buf.getvalue()
