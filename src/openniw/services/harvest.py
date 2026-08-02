"""OpenAlex citing-paper harvest with independence + published screening.

Deterministic and keyless. Retries with backoff; flushes incrementally after
every title so a failure never loses prior work. The agent does the judgment
afterwards (flagged-name review, full-text verification, depth scoring).
"""
import json
import pathlib
import time
import urllib.parse
import urllib.request

from .citations_pure import independence, title_sim

OPENALEX = "https://api.openalex.org"
UA = {"User-Agent": "OpenNIW/0.3 (open-source NIW tooling)"}


def _get(path: str, **params) -> dict:
    url = f"{OPENALEX}{path}?{urllib.parse.urlencode(params)}"
    last_exc: Exception | None = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=40) as resp:
                return json.load(resp)
        except Exception as exc:  # network blip / 429 — retry with backoff
            last_exc = exc
            time.sleep(2 * (attempt + 1))
    raise last_exc


def _authors(work: dict) -> list[str]:
    return [x["author"]["display_name"] for x in work.get("authorships", [])
            if x.get("author", {}).get("display_name")]


def harvest(titles: list[str], out_path: pathlib.Path,
            max_per_work: int = 200, log=print) -> dict:
    """Harvest citing papers for each title into out_path (JSON array).

    Returns a summary dict: {rows, independent, flagged, usable}.
    """
    out_path = pathlib.Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []

    def _flush() -> None:  # incremental: a failure never loses prior titles
        out_path.write_text(json.dumps(rows, indent=1, ensure_ascii=False))

    for title in titles:
        try:
            data = _get("/works", search=title[:250], **{"per-page": 1})
        except Exception as exc:
            log(f"  FAILED to resolve (network): {title[:60]}: {exc}")
            continue
        results = data.get("results") or []
        if not results or title_sim(title, results[0].get("display_name") or "") < 0.55:
            log(f"  NOT RESOLVED on OpenAlex: {title[:70]}")
            continue
        cited = results[0]
        cited_id = cited["id"].rsplit("/", 1)[-1]
        cited_authors = _authors(cited)
        log(f"  resolved: {cited['display_name'][:70]} "
            f"(cited_by {cited.get('cited_by_count')})")
        cursor, fetched = "*", 0
        while cursor and fetched < max_per_work:
            try:
                page = _get("/works", filter=f"cites:{cited_id}",
                            **{"per-page": 50, "cursor": cursor})
            except Exception as exc:
                log(f"  page fetch failed mid-harvest ({exc}); keeping "
                    f"{fetched} rows for this title")
                break
            cursor = (page.get("meta") or {}).get("next_cursor")
            batch = page.get("results") or []
            if not batch:
                break
            for w in batch:
                if fetched >= max_per_work:
                    break
                fetched += 1
                citing_authors = _authors(w)
                indep, flag = independence(cited_authors, citing_authors)
                src = (w.get("primary_location") or {}).get("source") or {}
                published = (src.get("type") != "repository"
                             and w.get("type") in ("article", "book-chapter",
                                                   "book", "review"))
                insts = []
                for x in w.get("authorships", []):
                    for inst in x.get("institutions", []):
                        insts.append({"author": x.get("author", {}).get("display_name"),
                                      "name": inst.get("display_name"),
                                      "country": inst.get("country_code")})
                rows.append({
                    "cited_title": cited["display_name"],
                    "citing_title": w.get("display_name"),
                    "venue": src.get("display_name"),
                    "venue_type": src.get("type"),
                    "year": w.get("publication_year"),
                    "doi": w.get("doi"),
                    "authors": citing_authors,
                    "institutions": insts,
                    "oa_pdf_url": ((w.get("best_oa_location") or {}) or {}).get("pdf_url"),
                    "published": published,
                    "independent": indep,
                    "same_surname_flag": flag,
                })
            time.sleep(0.2)  # be polite to the free API
        _flush()

    _flush()
    indep_n = sum(1 for r in rows if r["independent"])
    usable = sum(1 for r in rows
                 if r["independent"] and r["published"] and r["oa_pdf_url"])
    return {
        "rows": len(rows),
        "independent": indep_n,
        "flagged": sum(1 for r in rows if r["same_surname_flag"]),
        "usable": usable,
        "out": str(out_path),
    }
