"""AI drafting pipeline for case documents.

Order mirrors law-firm practice: PES first (it pins the frozen endeavor
sentence), then recommendation letters, then the petition letter (which cites
everything), then exhibit list and cover letter.

Every generator receives the full case bundle (profile, evaluation, evidence,
recommenders, prior documents) so facts stay consistent across artifacts.
"""
import json

from .. import prompts
from . import llm


def _bundle(case: dict, profile: dict, evaluation: dict | None,
            evidence: list[dict], recommenders: list[dict],
            documents: list[dict], answers: dict) -> str:
    """Serialize the case fact bundle passed to every drafting prompt."""
    docs_slim = [
        {
            "doc_type": d["doc_type"],
            "recommender_id": str(d.get("recommender_id") or ""),
            "content_md": (d.get("content_md") or "")[:30000],
        }
        for d in documents
    ]
    endeavor = case.get("endeavor") or {}
    payload = {
        "case": {
            "title": case.get("title"),
            "field": case.get("field"),
            # The frozen canonical endeavor — reuse VERBATIM in every document.
            "endeavor": {
                "sentence": endeavor.get("sentence") or endeavor.get("composed"),
                "pillars": endeavor.get("pillars"),
                "frozen": endeavor.get("frozen", False),
            },
        },
        "profile": profile,
        "evaluation_report": (evaluation or {}).get("report_md", ""),
        "evidence_items": [
            {
                "category": e["category"],
                "title": e["title"],
                "status": e["status"],
                "exhibit_no": e.get("exhibit_no"),
                "ai_notes": e.get("ai_notes"),
            }
            for e in evidence
        ],
        "recommenders": [
            {
                "id": str(r["id"]),
                "name": r["name"],
                "title": r.get("title"),
                "org": r.get("org"),
                "relationship": r.get("relationship"),
                "angle": r.get("angle"),
            }
            for r in recommenders
        ],
        "existing_documents": docs_slim,
        "interview_answers": answers,
    }
    return json.dumps(payload, ensure_ascii=False)[:200000]


async def draft_pes(bundle_args: dict) -> str:
    return await llm.complete(
        "Draft the Proposed Endeavor Statement for this case.\n\nCASE BUNDLE:\n"
        + _bundle(**bundle_args),
        system=prompts.load("pes"),
    )


async def draft_petition_letter(bundle_args: dict) -> str:
    return await llm.complete(
        "Draft the full Petition Letter for this case. The PES in "
        "existing_documents contains the canonical endeavor sentence — reuse "
        "it VERBATIM. Assign exhibit numbers consistent with the evidence "
        "items' exhibit_no where present.\n\nCASE BUNDLE:\n"
        + _bundle(**bundle_args),
        system=prompts.load("pl"),
    )


async def draft_reco_letter(bundle_args: dict, recommender: dict) -> str:
    return await llm.complete(
        "Draft the recommendation letter for this recommender:\n"
        + json.dumps(
            {
                "name": recommender["name"],
                "title": recommender.get("title"),
                "org": recommender.get("org"),
                "relationship": recommender.get("relationship"),
                "assigned_angle": recommender.get("angle"),
            },
            ensure_ascii=False,
        )
        + "\n\nCASE BUNDLE:\n" + _bundle(**bundle_args),
        system=prompts.load("reco_letter"),
    )


async def draft_exhibit_list(bundle_args: dict) -> str:
    return await llm.complete(
        "Produce the INDEX OF EXHIBITS for this case as markdown: three groups "
        "(Academic and Professional Background / Publications and Citations / "
        "Other), positional numbering, publications first-published-then-"
        "preprints with the standard entry format, a/b sub-letters for "
        "proof+context pairs. Use only evidence items with status 'provided' "
        "plus the PES (always an early exhibit) and the standard field-generic "
        "library (policy documents, Dhanasar, USCIS Policy Manual) at the end. "
        "If the petition letter exists in existing_documents, keep numbering "
        "consistent with its citations.\n\nCASE BUNDLE:\n"
        + _bundle(**bundle_args),
        effort="medium",
    )


async def draft_cover_letter(bundle_args: dict) -> str:
    answers = bundle_args.get("answers") or {}
    premium = answers.get("processing.premium") is True
    premium_note = (
        "This is a PREMIUM PROCESSING filing: title the letter 'Form I-140 "
        "(EB-2 National Interest Waiver) — Premium Processing Request', state "
        "that Form I-907 requesting Premium Processing Service is enclosed "
        "with its fee, and include Form I-907 in the enclosed-documents list "
        "(after G-1145, before Form I-140). "
        if premium else
        "Title the letter 'Form I-140 (EB-2 National Interest Waiver) — "
        "Original Submission'. "
    )
    return await llm.complete(
        "Draft a one-page filing cover letter for this I-140 NIW package, in "
        "the style of professionally prepared filings: USCIS lockbox address "
        "block at top, a bold title line identifying the submission, "
        "'Dear Sir or Madam:', one paragraph stating the enclosed petition — "
        "filed by the self-petitioner under EB-2 with a request for a "
        "National Interest Waiver pursuant to INA §203(b)(2)(B) and 8 C.F.R. "
        "§204.5(k), satisfying Matter of Dhanasar, 26 I&N Dec. 884 (AAO "
        "2016) — then a numbered ENCLOSED DOCUMENTS list in physical "
        "package order (payment authorization; Form G-1145; Form I-140 with "
        "filing fee; this cover letter; Form ETA-9089 Appendix A and signed "
        "Final Determination submitted in support of the NIW request; "
        "Petition Letter in Support of EB-2 National Interest Waiver; signed "
        "Proposed Endeavor Statement; support letters; Supporting Evidence "
        "(tabbed and indexed)), a closing request for approval, and "
        "'Respectfully submitted,' with the petitioner's name and "
        "'Self-Petitioner' beneath the signature line. " + premium_note +
        "Markdown.\n\n"
        "CASE BUNDLE:\n" + _bundle(**bundle_args),
        effort="medium",
    )


async def draft_rfe_response(bundle_args: dict, rfe_text: str) -> str:
    return await llm.complete(
        "RFE LETTER TEXT:\n" + rfe_text[:60000]
        + "\n\nCASE BUNDLE:\n" + _bundle(**bundle_args),
        system=prompts.load("rfe"),
    )


DRAFTERS = {
    "pes": draft_pes,
    "petition_letter": draft_petition_letter,
    "exhibit_list": draft_exhibit_list,
    "cover_letter": draft_cover_letter,
}
