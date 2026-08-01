"""Evidence checklist generation.

A fixed taxonomy (derived from real successful filings) is personalized per
case: items the system already derived are marked provided; items irrelevant to
the profile are dropped; AI adds concrete how-to notes.
"""
import json

from . import llm

# (category, title, description, how-to note)
BASE_CHECKLIST: list[tuple[str, str, str, str]] = [
    ("identity", "Passport biographic page", "Identity and citizenship proof.",
     "Scan the photo page of your current passport."),
    ("identity", "Current U.S. status documents", "Visa, I-94, I-20/DS-2019 or approval notices, if in the U.S.",
     "Download your latest I-94 from the CBP website."),
    ("degree", "Diplomas (all degrees)", "Highest degree establishes EB-2 eligibility.",
     "Scan originals; non-U.S. degrees may need a credential evaluation."),
    ("degree", "Transcripts", "Official transcripts for each degree.",
     "Request from the registrar; scans of official copies are fine."),
    ("cv", "Up-to-date CV", "Exhibit 1 of the filing.",
     "Include education, publications (bold your name; mark co-first authorship), experience, professional service."),
    ("publications", "Publication PDFs", "One exhibit per paper: published first, then preprints.",
     "Use the official published version, not the preprint, whenever it exists."),
    ("publications", "Acceptance proof for in-press papers", "Acceptance emails or review-forum pages.",
     "Export acceptance emails to PDF."),
    ("citations", "Citation record", "Google Scholar profile printout showing totals and per-paper counts.",
     "Print your Scholar profile page to PDF (logged out)."),
    ("citations", "Citation-percentile support", "Field-year average citation data for percentile arguments.",
     "The system computes percentile arguments where data allows."),
    ("citations", "Notable citing papers", "3+ third-party papers that used/implemented/extended your work.",
     "Prefer formally published papers with no shared co-authors; the deeper the use, the better. Avoid citations that criticize or merely list your work."),
    ("peer_review", "Peer-review service evidence", "Email trails for each completed review.",
     "For each review: invitation, acceptance/assignment, and completion emails, exported to PDF, grouped by venue."),
    ("awards", "Awards & honors", "Award notices plus public pages establishing selectivity.",
     "Capture the official award page and any email; note how many were selected out of how many."),
    ("funding", "Research funding evidence", "Award pages for grants you worked under.",
     "Public award-abstract pages; you 'participated in projects funded by' the award — the system phrases this safely."),
    ("open_source", "Open-source adoption", "Repository pages showing stars/forks/PRs from others.",
     "Print the repo main page and pull-request list to PDF, logged out, with visible date."),
    ("patents", "Patents / IP", "Filed or granted patents, plus any licensing evidence.",
     "Unlicensed patents carry limited weight; licensing/commercialization evidence is what counts."),
    ("media", "Media & expert commentary", "Coverage of you or your work.",
     "Save articles to PDF; foreign-language items need certified English translations."),
    ("endeavor", "Proposed endeavor worksheet", "The six-field definition of each planned project.",
     "Completed in the AI interview: need, scenario, implementation path, beneficiaries, impact, means of execution."),
    ("employment", "Employment verification letter", "Title, start date, salary, duties, % research.",
     "The system drafts a template your employer can adapt and sign."),
    ("recommenders", "Recommender list", "3-6 candidates: independent (cited your work) + dependent (first-hand).",
     "Completed in the AI interview; don't contact anyone until drafts are ready."),
]


def base_items() -> list[dict]:
    return [
        {"category": c, "title": t, "description": d, "ai_notes": n}
        for c, t, d, n in BASE_CHECKLIST
    ]


PERSONALIZE_SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "status": {
                        "type": "string",
                        "enum": ["suggested", "needed", "provided", "na"],
                    },
                    "ai_notes": {"type": "string"},
                },
                "required": ["category", "title", "status"],
            },
        }
    },
    "required": ["items"],
}


async def personalize(profile: dict, evaluation_md: str) -> list[dict]:
    """LLM pass: adapt the base checklist to this applicant."""
    result = await llm.complete(
        "Adapt this NIW evidence checklist to the applicant. Mark items the "
        "profile already substantiates as 'provided', clearly irrelevant ones "
        "'na', high-priority gaps 'needed', the rest 'suggested'. Rewrite "
        "ai_notes to be specific to this applicant (name actual venues, repos, "
        "awards from the profile). Add applicant-specific items the evaluation "
        "recommends (e.g. letters of interest, government interest) with "
        "status 'needed'.\n\nBase checklist:\n"
        + json.dumps(base_items(), ensure_ascii=False)
        + "\n\nProfile:\n" + json.dumps(profile, ensure_ascii=False)[:60000]
        + "\n\nEvaluation:\n" + evaluation_md[:20000],
        schema=PERSONALIZE_SCHEMA,
    )
    return result["items"]
