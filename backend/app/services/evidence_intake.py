"""Upload-and-forget evidence intake.

Any uploaded PDF/image is classified, matched to the checklist, key fields
are extracted into the canonical fact table, and the exhibit is date-classed
against the filing date (pre-filing evidence is what wins cases).
"""
import datetime as dt
import json

from .. import db
from . import llm

INTAKE_SCHEMA = {
    "type": "object",
    "properties": {
        "doc_kind": {"type": "string"},
        "category": {
            "type": "string",
            "enum": ["identity", "degree", "cv", "publications", "citations",
                     "peer_review", "awards", "funding", "open_source",
                     "patents", "media", "endeavor", "employment",
                     "recommenders", "other"],
        },
        "title": {"type": "string"},
        "document_date": {"type": "string", "description": "YYYY-MM-DD or empty"},
        "summary": {"type": "string"},
        "facts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "value": {"type": "string"},
                    "as_of": {"type": "string"},
                },
                "required": ["key", "value"],
            },
        },
        "quality_notes": {"type": "string"},
    },
    "required": ["category", "title", "summary"],
}


async def process_upload(case_id, item_id, filename: str, text: str | None) -> dict:
    """Classify + extract; update the evidence item and the fact table."""
    if not text:
        return {"classified": False}
    result = await llm.complete(
        "Classify this document uploaded as evidence for an EB-2 NIW petition "
        "and extract its key facts. doc_kind examples: diploma, transcript, "
        "peer-review thank-you email, award notification, grant award page, "
        "GitHub repository page, media article, employment letter, citation "
        "report, published paper. facts: durable case facts a petition might "
        "state (e.g. key='award_selectivity', value='60 of 3000 submissions "
        "(2%)'; key='citations_total', value='412', as_of='2026-07-01'; "
        "key='salary', value='$120,000/yr'). Extract only what the text "
        "supports. quality_notes: anything that weakens it as USCIS evidence "
        "(missing URL, missing date, name not visible, unofficial copy...).\n\n"
        f"Filename: {filename}\n\nDocument text (extract):\n{text[:25000]}",
        schema=INTAKE_SCHEMA,
        effort="medium",
    )

    case = await db.fetchrow("select filed_date from cases where id=$1", case_id)
    date_class = "unknown"
    doc_date = None
    raw_date = (result.get("document_date") or "").strip()
    if raw_date:
        try:
            doc_date = dt.date.fromisoformat(raw_date[:10])
        except ValueError:
            doc_date = None
    if doc_date is not None:
        filed = case["filed_date"] if case else None
        if filed is None:
            date_class = "pre_filing"  # not yet filed: everything counts
        else:
            date_class = "pre_filing" if doc_date <= filed else "post_filing"

    notes = result.get("summary", "")
    if result.get("quality_notes"):
        notes += f"\n⚠ {result['quality_notes']}"
    await db.execute(
        """update evidence_items
           set extracted=$3, date_class=$4,
               ai_notes=left(coalesce(ai_notes,'') || E'\\n[intake] ' || $5, 4000)
           where id=$1 and case_id=$2""",
        item_id, case_id, result, date_class, notes,
    )
    for fact in result.get("facts") or []:
        as_of = None
        try:
            if fact.get("as_of"):
                as_of = dt.date.fromisoformat(str(fact["as_of"])[:10])
        except ValueError:
            pass
        await db.execute(
            """insert into case_facts(case_id, category, key, value, as_of, source)
               values($1,$2,$3,$4,$5,$6)""",
            case_id, result.get("category", "other"),
            str(fact["key"])[:200], str(fact["value"])[:2000],
            as_of, f"upload:{filename}"[:300],
        )
    return {
        "classified": True,
        "category": result.get("category"),
        "doc_kind": result.get("doc_kind"),
        "date_class": date_class,
        "facts": len(result.get("facts") or []),
        "quality_notes": result.get("quality_notes"),
    }
