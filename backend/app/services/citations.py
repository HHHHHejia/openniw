"""The citation pipeline — the most labor-intensive part of a NIW case,
fully automated.

Stages (mirroring how a successful RFE response was actually prepared):
  1. harvest     — resolve the applicant's works on OpenAlex, pull every
                   citing paper with authorships/venue/OA links
  2. screen      — independence (no shared author; same-surname collisions
                   flagged for human review) + published-only filter
  3. verify+score— download OA full text, confirm the citation actually
                   appears, extract the citing context, LLM-score depth of
                   use (implemented / compared-favorably / utilized /
                   verified; 1–9) and quarantine negative citations
  4. select      — portfolio selection across cited works
  5. deliver     — highlighted PDFs + the Citation Examples control file +
                   independent-recommender candidates from citing authors

Doctrine encoded here (from docs/analysis/rfe-playbook.md): HOW > WHO;
never use negative citations; published citing papers only; verify every
claimed citation exists in the full text; state the independence methodology.
"""
import asyncio
import io
import json
import re
import unicodedata

import fitz  # pymupdf
import httpx

from .. import db
from . import llm, storage

OPENALEX = "https://api.openalex.org"
UA = {"User-Agent": "OpenNIW/0.2 (open-source NIW tooling; mailto:openniw@example.org)"}

MAX_CITING_PER_WORK = 200
MAX_PDF_BYTES = 20 * 1024 * 1024


# ---------------------------------------------------------------------------
# Author-name handling
# ---------------------------------------------------------------------------

def _norm(name: str) -> str:
    return unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()


def _fam_init(display_name: str) -> tuple[str, str]:
    """('doe', 'j') from 'Jane Doe'. OpenAlex display names are given-first."""
    parts = [p for p in _norm(display_name).replace(",", " ").split() if p]
    if not parts:
        return ("", "")
    return (parts[-1], parts[0][:1])


def independence(cited_authors: list[str], citing_authors: list[str]) -> tuple[bool, bool]:
    """(independent, same_surname_flag).

    Exact normalized full-name match -> dependent.
    Family+initial match (different full name, e.g. John/Jane Doe) ->
      conservatively dependent AND flagged for manual full-name review.
    Family-only match -> independent but flagged.
    """
    cited_full = {_norm(a) for a in cited_authors}
    cited_fi = {_fam_init(a) for a in cited_authors}
    cited_fams = {f for f, _ in cited_fi}
    flag = False
    for a in citing_authors:
        if _norm(a) in cited_full:
            return (False, False)
    for a in citing_authors:
        f, i = _fam_init(a)
        if (f, i) in cited_fi:
            return (False, True)
        if f in cited_fams:
            flag = True
    return (True, flag)


# ---------------------------------------------------------------------------
# Stage 1-2: harvest from OpenAlex
# ---------------------------------------------------------------------------

async def _oa_get(http: httpx.AsyncClient, path: str, **params) -> dict:
    resp = await http.get(f"{OPENALEX}{path}", params=params, headers=UA, timeout=40)
    resp.raise_for_status()
    return resp.json()


def _work_authors(work: dict) -> list[str]:
    return [a["author"]["display_name"] for a in work.get("authorships", [])
            if a.get("author", {}).get("display_name")]


def _work_institutions(work: dict) -> list[dict]:
    out = []
    for a in work.get("authorships", []):
        for inst in a.get("institutions", []):
            out.append({
                "author": a.get("author", {}).get("display_name"),
                "name": inst.get("display_name"),
                "country": inst.get("country_code"),
            })
    return out


def _is_published(work: dict) -> bool:
    src = (work.get("primary_location") or {}).get("source") or {}
    if src.get("type") == "repository":  # arXiv, SSRN, ...
        return False
    return work.get("type") in ("article", "book-chapter", "book", "review")


async def harvest(case_id, publication_titles: list[str]) -> dict:
    """Resolve each of the applicant's papers on OpenAlex and pull its citing
    works. Inserts citing_papers rows (idempotent per citing/cited pair)."""
    stats = {"cited_resolved": 0, "citing_found": 0, "inserted": 0, "skipped_existing": 0}
    async with httpx.AsyncClient() as http:
        for title in publication_titles[:20]:
            data = await _oa_get(http, "/works", search=title[:250], **{"per-page": 1})
            results = data.get("results") or []
            if not results:
                continue
            cited = results[0]
            # Guard against fuzzy-search mismatches.
            if _title_sim(title, cited.get("display_name") or "") < 0.55:
                continue
            stats["cited_resolved"] += 1
            cited_id = cited["id"].rsplit("/", 1)[-1]
            cited_authors = _work_authors(cited)

            cursor = "*"
            fetched = 0
            while cursor and fetched < MAX_CITING_PER_WORK:
                page = await _oa_get(
                    http, "/works",
                    filter=f"cites:{cited_id}",
                    **{"per-page": 50, "cursor": cursor},
                )
                cursor = (page.get("meta") or {}).get("next_cursor")
                for w in page.get("results") or []:
                    fetched += 1
                    stats["citing_found"] += 1
                    citing_authors = _work_authors(w)
                    indep, flag = independence(cited_authors, citing_authors)
                    oa_pdf = ((w.get("best_oa_location") or {}) or {}).get("pdf_url")
                    src = (w.get("primary_location") or {}).get("source") or {}
                    inserted = await db.fetchval(
                        """insert into citing_papers
                           (case_id, cited_title, cited_openalex_id,
                            citing_openalex_id, citing_title, citing_authors,
                            citing_institutions, citing_venue, citing_venue_type,
                            citing_year, doi, oa_pdf_url, published,
                            independent, same_surname_flag)
                           values($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15)
                           on conflict (case_id, citing_openalex_id, cited_openalex_id)
                           do nothing returning id""",
                        case_id, cited.get("display_name") or title, cited_id,
                        w["id"].rsplit("/", 1)[-1],
                        w.get("display_name") or "(untitled)",
                        citing_authors, _work_institutions(w),
                        src.get("display_name"), src.get("type"),
                        w.get("publication_year"), w.get("doi"),
                        oa_pdf, _is_published(w), indep, flag,
                    )
                    if inserted:
                        stats["inserted"] += 1
                    else:
                        stats["skipped_existing"] += 1
                if not (page.get("results") or []):
                    break
    return stats


def _title_sim(a: str, b: str) -> float:
    aw, bw = set(_norm(a).split()), set(_norm(b).split())
    if not aw or not bw:
        return 0.0
    return len(aw & bw) / max(len(aw), len(bw))


# ---------------------------------------------------------------------------
# Stage 3: verify in full text + LLM depth scoring
# ---------------------------------------------------------------------------

SCORE_SCHEMA = {
    "type": "object",
    "properties": {
        "cites_target": {"type": "boolean"},
        "use_type": {
            "type": "string",
            "enum": ["implemented", "compared_favorably", "utilized", "verified",
                     "extensive", "moderate", "background", "passing"],
        },
        "score": {"type": "integer", "minimum": 1, "maximum": 9},
        "negative": {"type": "boolean"},
        "best_quote": {"type": "string"},
        "rationale": {"type": "string"},
    },
    "required": ["cites_target", "use_type", "score", "negative"],
}


def _citation_contexts(full_text: str, surname: str, cited_title: str) -> list[str]:
    """Windows of text around likely citations to the applicant's work."""
    contexts: list[str] = []
    needles = [surname] if surname else []
    title_words = [w for w in _norm(cited_title).split() if len(w) > 6][:3]
    needles.extend(title_words)
    lowered = full_text.lower()
    seen_spans: list[tuple[int, int]] = []
    for needle in needles:
        for m in re.finditer(re.escape(needle.lower()), lowered):
            start, end = max(0, m.start() - 450), min(len(full_text), m.end() + 450)
            if any(s <= m.start() <= e for s, e in seen_spans):
                continue
            seen_spans.append((start, end))
            contexts.append(full_text[start:end])
            if len(contexts) >= 6:
                return contexts
    return contexts


async def verify_and_score(row: dict, applicant_surname: str) -> dict:
    """Download the citing paper's OA PDF, confirm the citation exists in the
    body, and LLM-score the depth of use. Returns column updates."""
    if not row.get("oa_pdf_url"):
        return {"verified_in_text": None, "status": "verified",
                "reject_reason": "no OA full text available"}
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=60) as http:
            resp = await http.get(row["oa_pdf_url"], headers=UA)
            resp.raise_for_status()
            content = resp.content[:MAX_PDF_BYTES]
        from .scraping import extract_pdf_text
        text = extract_pdf_text(content, max_chars=250000)
    except Exception as exc:
        return {"verified_in_text": None, "status": "verified",
                "reject_reason": f"pdf fetch/extract failed: {exc}"[:300]}

    pdf_rel = storage.save(str(row["case_id"]), f"citing_{row['citing_openalex_id']}.pdf", content)
    contexts = _citation_contexts(text, applicant_surname, row["cited_title"])
    if not contexts:
        return {"verified_in_text": False, "status": "verified", "pdf_path": pdf_rel,
                "reject_reason": "citation not found in full text (index false positive)"}

    result = await llm.complete(
        "You are scoring a citation for an EB-2 NIW petition using the "
        "HOW > WHO doctrine. The applicant's cited paper: "
        f"\"{row['cited_title']}\" (surname: {applicant_surname}).\n"
        f"The citing paper: \"{row['citing_title']}\" ({row.get('citing_venue')}, "
        f"{row.get('citing_year')}).\n\n"
        "Citation contexts extracted from the citing paper's full text:\n\n"
        + "\n---\n".join(contexts)
        + "\n\nAssess: does this text actually cite/use the applicant's paper "
        "(cites_target)? Classify depth of use: implemented (adopts the "
        "methods/models), compared_favorably (comparison showing the cited "
        "work's value), utilized (used to build something), verified "
        "(confirms the results), extensive/moderate/background/passing. "
        "Score 1-9 (9 = the cited work is an explicit analytical framework "
        "used across sections; 5 = one dedicated sentence; 1-2 = grouped "
        "passing mention). negative=true if the context frames the cited "
        "work as limited, superseded, or among methods that 'fail to' do "
        "something. best_quote = the single most favorable verbatim citing "
        "sentence.",
        schema=SCORE_SCHEMA,
        effort="medium",
    )
    if not result.get("cites_target"):
        return {"verified_in_text": False, "status": "verified", "pdf_path": pdf_rel,
                "reject_reason": "context does not actually cite the work"}
    return {
        "verified_in_text": True,
        "status": "scored",
        "pdf_path": pdf_rel,
        "quote_context": (result.get("best_quote") or contexts[0])[:2000],
        "use_type": result.get("use_type"),
        "score": result.get("score"),
        "negative": bool(result.get("negative")),
    }


async def run_verification(case_id, applicant_surname: str, limit: int = 40) -> dict:
    """Verify+score the most promising screened rows: independent, published,
    with OA full text, not yet processed."""
    rows = await db.fetch(
        """select * from citing_papers
           where case_id=$1 and status='harvested'
             and independent and published and oa_pdf_url is not null
           order by citing_year desc nulls last limit $2""",
        case_id, limit,
    )
    done = 0
    sem = asyncio.Semaphore(4)

    async def work(row):
        nonlocal done
        async with sem:
            updates = await verify_and_score(dict(row), applicant_surname)
            sets = ", ".join(f"{k}=${i + 2}" for i, k in enumerate(updates))
            await db.execute(
                f"update citing_papers set {sets} where id=$1",
                row["id"], *updates.values(),
            )
            done += 1

    await asyncio.gather(*(work(r) for r in rows))
    return {"processed": done}


# ---------------------------------------------------------------------------
# Stage 4: portfolio selection
# ---------------------------------------------------------------------------

async def select_portfolio(case_id, target: int = 10) -> dict:
    """Pick the strongest examples with coverage across cited works.
    Never selects negative, unverified, or unpublished rows."""
    rows = await db.fetch(
        """select * from citing_papers
           where case_id=$1 and status in ('scored','selected')
             and verified_in_text and not negative and independent and published
           order by score desc nulls last""",
        case_id,
    )
    await db.execute(
        "update citing_papers set status='scored' where case_id=$1 and status='selected'",
        case_id,
    )
    per_cited: dict[str, int] = {}
    chosen = []
    # Round 1: max 2 per cited work for coverage; round 2: fill by score.
    for row in rows:
        if len(chosen) >= target:
            break
        if (row["score"] or 0) < 5:
            continue
        if per_cited.get(row["cited_openalex_id"], 0) >= 2:
            continue
        chosen.append(row)
        per_cited[row["cited_openalex_id"]] = per_cited.get(row["cited_openalex_id"], 0) + 1
    for row in rows:
        if len(chosen) >= target:
            break
        if row in chosen or (row["score"] or 0) < 5:
            continue
        chosen.append(row)
    for row in chosen:
        await db.execute(
            "update citing_papers set status='selected' where id=$1", row["id"]
        )
    return {"selected": len(chosen), "coverage": per_cited}


# ---------------------------------------------------------------------------
# Stage 5: deliverables
# ---------------------------------------------------------------------------

def highlight_pdf(pdf_bytes: bytes, needles: list[str]) -> bytes:
    """Highlight every occurrence of the needles (applicant surname, cited
    title fragments) — in-text citations and the reference entry, nothing else."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page in doc:
        for needle in needles:
            if not needle or len(needle) < 3:
                continue
            for rect in page.search_for(needle, quads=False):
                page.add_highlight_annot(rect)
    out = doc.tobytes()
    doc.close()
    return out


async def build_deliverables(case_id, applicant_surname: str) -> dict:
    """Numbered highlighted PDFs + the Citation Examples control document."""
    rows = await db.fetch(
        """select * from citing_papers where case_id=$1 and status='selected'
           order by score desc nulls last""",
        case_id,
    )
    entries = []
    for i, row in enumerate(rows, 1):
        entry = {
            "n": i,
            "cited_paper": row["cited_title"],
            "citing_paper": row["citing_title"],
            "venue": row["citing_venue"],
            "year": row["citing_year"],
            "doi": row["doi"],
            "use_type": row["use_type"],
            "score": row["score"],
            "quote": row["quote_context"],
            "authors": row["citing_authors"],
        }
        if row["pdf_path"]:
            try:
                raw = storage.read(row["pdf_path"])
                needles = [applicant_surname] + [
                    w for w in row["cited_title"].split() if len(w) > 7
                ][:2]
                marked = highlight_pdf(raw, needles)
                short = re.sub(r"[^A-Za-z0-9]+", "_", row["citing_title"])[:40]
                rel = storage.save(
                    str(case_id), f"{i:02d}_{short}_HIGHLIGHTED.pdf", marked
                )
                entry["highlighted_pdf"] = rel
                await db.execute(
                    "update citing_papers set pdf_path=$2 where id=$1",
                    row["id"], rel,
                )
            except Exception:
                pass
        entries.append(entry)

    doc_md = await llm.complete(
        "Produce a 'Citation Examples' summary document (markdown) for an "
        "EB-2 NIW petition from these verified, scored citation examples. "
        "For each numbered example use this structure:\n"
        "### Example N\n"
        "**Cited Paper(s):** ...\n**Citing Paper:** full citation\n"
        "**Citing Article Type:** original research/review/...\n"
        "**Citation to Your Work:** the verbatim quote\n"
        "**Citing Article's Objectives:** 3-4 sentences\n"
        "**How and Why the Work Was Used:** 4-5 sentences ending with an "
        "explicit statement of the function the cited work served\n"
        "**Findings & Relation to the Cited Work:** 4-5 sentences\n\n"
        "Plain officer-readable English; gloss technical terms inline; do "
        "NOT emphasize citer prestige (HOW > WHO). Start with a one-paragraph "
        "independence-methodology note (no shared authors, matched on family "
        "name + first initial).\n\nDATA:\n"
        + json.dumps(entries, ensure_ascii=False, default=str)[:150000],
    )
    version = await db.fetchval(
        """select coalesce(max(version),0)+1 from documents
           where case_id=$1 and doc_type='citation_examples'""",
        case_id,
    )
    doc_id = await db.fetchval(
        """insert into documents(case_id, doc_type, version, content_md)
           values($1,'citation_examples',$2,$3) returning id""",
        case_id, version, doc_md,
    )
    return {"document_id": str(doc_id), "examples": len(entries),
            "highlighted_pdfs": sum(1 for e in entries if e.get("highlighted_pdf"))}


async def recommender_candidates(case_id) -> list[dict]:
    """Independent-recommender candidates from authors of selected citing
    papers. Strongest: can discuss >=2 notable citations; U.S. institutions
    preferred."""
    rows = await db.fetch(
        """select * from citing_papers where case_id=$1 and status='selected'""",
        case_id,
    )
    by_author: dict[str, dict] = {}
    for row in rows:
        insts = {i.get("author"): i for i in (row["citing_institutions"] or [])}
        for author in row["citing_authors"] or []:
            rec = by_author.setdefault(author, {
                "name": author, "papers": [], "institutions": set(), "us": False,
            })
            rec["papers"].append(row["citing_title"])
            inst = insts.get(author)
            if inst and inst.get("name"):
                rec["institutions"].add(inst["name"])
                if inst.get("country") == "US":
                    rec["us"] = True
    out = []
    for rec in by_author.values():
        out.append({
            "name": rec["name"],
            "citing_papers": rec["papers"],
            "n_citations_discussable": len(rec["papers"]),
            "institutions": sorted(rec["institutions"]),
            "us_based": rec["us"],
        })
    out.sort(key=lambda r: (-r["n_citations_discussable"], not r["us_based"]))
    return out[:20]
