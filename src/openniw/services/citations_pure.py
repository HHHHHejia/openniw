"""Deterministic citation-pipeline helpers (no LLM, no network, no DB).

The agent does the judgment (depth scoring, negative-citation quarantine,
portfolio selection); these are the mechanical parts it delegates.
"""
import re
import unicodedata


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

def is_published(work: dict) -> bool:
    """Formally published (no preprints/posters) per OpenAlex metadata."""
    src = (work.get("primary_location") or {}).get("source") or {}
    if src.get("type") == "repository":  # arXiv, SSRN, ...
        return False
    return work.get("type") in ("article", "book-chapter", "book", "review")


def citation_contexts(full_text: str, surname: str, cited_title: str) -> list[str]:
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


def highlight_pdf(pdf_bytes: bytes, needles: list[str]) -> bytes:
    """Highlight every occurrence of the needles (applicant surname, cited
    title fragments) — in-text citations and the reference entry."""
    import fitz  # pymupdf

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
