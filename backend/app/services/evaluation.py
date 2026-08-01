"""Free evaluation: gather sources -> consolidate profile -> evaluate."""
import asyncio
import json

from .. import prompts
from . import llm, scraping

TIER_SCHEMA = {
    "type": "object",
    "properties": {
        "tier": {
            "type": "string",
            "enum": ["strong", "promising", "borderline", "not-yet"],
        },
        "prong_scores": {
            "type": "object",
            "properties": {
                "prong1": {"type": "integer", "minimum": 1, "maximum": 5},
                "prong2": {"type": "integer", "minimum": 1, "maximum": 5},
                "prong3": {"type": "integer", "minimum": 1, "maximum": 5},
            },
        },
    },
    "required": ["tier"],
}


async def gather_sources(
    scholar_url: str | None,
    homepage_url: str | None,
    cv_text: str | None,
    linkedin_text: str | None,
    notes: str | None,
) -> dict:
    """Fetch whatever the user linked; tolerate individual failures."""
    sources: dict = {}
    errors: dict = {}

    async def _try(key: str, coro) -> None:
        try:
            sources[key] = await coro
        except Exception as exc:  # network/parse failures must not kill the eval
            errors[key] = str(exc)

    tasks = []
    if scholar_url:
        tasks.append(_try("scholar", scraping.fetch_scholar_profile(scholar_url)))
    if homepage_url:
        tasks.append(_try("homepage", scraping.fetch_homepage(homepage_url)))
    if tasks:
        await asyncio.gather(*tasks)
    if cv_text:
        sources["cv_text"] = cv_text[:40000]
    if linkedin_text:
        sources["linkedin_text"] = linkedin_text[:40000]
    if notes:
        sources["notes"] = notes[:10000]
    if errors:
        sources["_fetch_errors"] = errors
    return sources


async def consolidate_profile(sources: dict, basics: dict) -> dict:
    """LLM pass: raw sources -> structured profile JSON."""
    payload = {"applicant_basics": basics, "sources": sources}
    return await llm.complete(
        "Consolidate the following raw material into the profile JSON.\n\n"
        + json.dumps(payload, ensure_ascii=False)[:120000],
        system=prompts.load("profile_extract"),
        schema={"type": "object"},
    )


async def evaluate(profile: dict, basics: dict) -> dict:
    """LLM pass: structured profile -> evaluation report + tier."""
    user_prompt = (
        "Evaluate this applicant for an EB-2 NIW self-petition.\n\n"
        "Applicant basics:\n" + json.dumps(basics, ensure_ascii=False) + "\n\n"
        "Consolidated profile:\n" + json.dumps(profile, ensure_ascii=False)[:100000]
    )
    report_md = await llm.complete(user_prompt, system=prompts.load("evaluation"))
    scored = await llm.complete(
        "Based on this NIW evaluation, output the tier and 1-5 prong scores.\n\n"
        + report_md,
        schema=TIER_SCHEMA,
        effort="low",
    )
    return {
        "report_md": report_md,
        "tier": scored.get("tier", "borderline"),
        "prong_scores": scored.get("prong_scores", {}),
    }
