"""Single chokepoint for all OpenAI calls.

Model and reasoning effort are env-configured (defaults: gpt-5.6-luna, xhigh).
Structured tasks pass a JSON schema; we try the Responses API structured-output
format first and fall back to instruction-based JSON if the SDK/model rejects it.
"""
import json
import re
from typing import Any

from openai import AsyncOpenAI

from ..config import get_settings

_client: AsyncOpenAI | None = None


def client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=get_settings().openai_api_key)
    return _client


async def complete(
    prompt: str,
    system: str = "",
    schema: dict | None = None,
    effort: str | None = None,
) -> Any:
    """Run one completion. Returns text, or a parsed object when `schema` given."""
    settings = get_settings()
    effort = effort or settings.openai_reasoning_effort
    messages: list[dict] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    kwargs: dict = {
        "model": settings.openai_model,
        "input": messages,
        "reasoning": {"effort": effort},
    }
    if schema is not None:
        kwargs["text"] = {
            "format": {
                "type": "json_schema",
                "name": "result",
                "schema": schema,
                "strict": False,
            }
        }
    try:
        resp = await client().responses.create(**kwargs)
        text = resp.output_text
    except Exception:
        if schema is None:
            raise
        # Fallback: ask for JSON in-band.
        messages[-1]["content"] += (
            "\n\nRespond ONLY with a JSON object matching this schema:\n"
            + json.dumps(schema)
        )
        resp = await client().responses.create(
            model=settings.openai_model,
            input=messages,
            reasoning={"effort": effort},
        )
        text = resp.output_text

    if schema is None:
        return text
    return _parse_json(text)


def _parse_json(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Strip markdown fences or surrounding prose.
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        return json.loads(m.group(0))
    raise ValueError(f"Model did not return JSON: {text[:200]}")
