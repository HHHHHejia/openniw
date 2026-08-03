#!/usr/bin/env python3
"""Harvest citing papers for the applicant's publications from OpenAlex.

Stdlib only, no API key needed. The AGENT does the judgment work afterwards
(independence review of flagged names, depth-of-use scoring from full text);
this script does the deterministic part: harvest + metadata + independence
screen + published-only classification.

Usage:
    python3 harvest_citations.py "Paper title one" "Paper title two" ... \
        [--out citations/harvest.json] [--max-per-work 200]

Output JSON per citing paper:
    cited_title, citing_title, venue, venue_type, year, doi, authors,
    institutions, oa_pdf_url, published, independent, same_surname_flag
Independence rule: no shared author between citing and cited paper, matched
on exact full name; family+initial collisions are conservatively marked
dependent AND flagged for manual review; family-only matches flagged.
"""
import json
import pathlib
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

OPENALEX = "https://api.openalex.org"
UA = {"User-Agent": "OpenNIW-skill/1.0 (open-source NIW tooling)"}


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


# --- BEGIN SYNC: citation screening (source of truth: src/openniw/services/citations_pure.py) ---
def _norm(name: str) -> str:
    return unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()


def _fam_init(name: str) -> tuple[str, str]:
    n = _norm(name)
    if "," in n:  # "Last, First" style
        family, _, given = n.partition(",")
        family = family.strip().split()[-1] if family.strip() else ""
        given = given.strip()
        return (family, given[:1] if given else "")
    parts = n.split()
    return (parts[-1], parts[0][:1]) if parts else ("", "")


def independence(cited: list[str], citing: list[str]) -> tuple[bool, bool]:
    """(independent, same_surname_flag).

    Exact full-name match => dependent. Family+initial collision =>
    conservatively dependent AND flagged. Family-only match => independent
    but flagged for manual review.
    """
    cited_full = {_norm(a) for a in cited}
    cited_fi = {_fam_init(a) for a in cited}
    cited_fams = {f for f, _ in cited_fi}
    flag = False
    for a in citing:
        if _norm(a) in cited_full:
            return (False, False)
    for a in citing:
        f, i = _fam_init(a)
        if (f, i) in cited_fi:
            return (False, True)
        if f in cited_fams:
            flag = True
    return (True, flag)


def title_sim(a: str, b: str) -> float:
    aw, bw = set(_norm(a).split()), set(_norm(b).split())
    return len(aw & bw) / max(len(aw), len(bw)) if aw and bw else 0.0

# --- END SYNC: citation screening ---
_title_sim = title_sim  # back-compat alias for main()


def _authors(work: dict) -> list[str]:
    return [x["author"]["display_name"] for x in work.get("authorships", [])
            if x.get("author", {}).get("display_name")]


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(
        description="Harvest citing papers from OpenAlex for petition evidence")
    ap.add_argument("titles", nargs="+", help="the applicant's paper titles")
    ap.add_argument("--out", default="citations/harvest.json")
    ap.add_argument("--max-per-work", type=int, default=200)
    ns = ap.parse_args()
    out_path = pathlib.Path(ns.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []

    def _flush() -> None:  # incremental: a failure never loses prior titles
        out_path.write_text(json.dumps(rows, indent=1, ensure_ascii=False))

    for title in ns.titles:
        try:
            data = _get("/works", search=title[:250], **{"per-page": 1})
        except Exception as exc:
            print(f"  FAILED to resolve (network): {title[:60]}: {exc}")
            continue
        results = data.get("results") or []
        if not results or _title_sim(title, results[0].get("display_name") or "") < 0.55:
            print(f"  NOT RESOLVED on OpenAlex: {title[:70]}")
            continue
        cited = results[0]
        cited_id = cited["id"].rsplit("/", 1)[-1]
        cited_authors = _authors(cited)
        print(f"  resolved: {cited['display_name'][:70]} "
              f"(cited_by {cited.get('cited_by_count')})")
        cursor, fetched = "*", 0
        while cursor and fetched < ns.max_per_work:
            try:
                page = _get("/works", filter=f"cites:{cited_id}",
                            **{"per-page": 50, "cursor": cursor})
            except Exception as exc:
                print(f"  page fetch failed mid-harvest ({exc}); keeping "
                      f"{fetched} rows for this title")
                break
            cursor = (page.get("meta") or {}).get("next_cursor")
            batch = page.get("results") or []
            if not batch:
                break
            for w in batch:
                if fetched >= ns.max_per_work:
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
    print(f"\n{len(rows)} citing papers -> {out_path}")
    print(f"  independent: {indep_n} "
          f"({round(100 * indep_n / len(rows), 1) if rows else 0}%)")
    print(f"  flagged for same-surname review: "
          f"{sum(1 for r in rows if r['same_surname_flag'])}")
    print(f"  usable pool (independent + published + open-access PDF): {usable}")
    print("\nNext: the agent reviews flagged names, downloads OA PDFs for the "
          "usable pool, verifies each citation appears in the full text, and "
          "scores depth of use (see references/evidence.md).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
