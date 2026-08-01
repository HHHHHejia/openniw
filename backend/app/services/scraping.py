"""Automated profile ingestion.

Philosophy: the user gives us links, we do the paperwork.
- Google Scholar profile pages are public server-rendered HTML -> parse directly.
- Personal homepages -> fetch and reduce to readable text.
- LinkedIn is auth-walled -> the user uploads LinkedIn's own "Save to PDF"
  export (or pastes text); we extract text here and let the LLM structure it.
- CV PDFs -> text extraction via pypdf.
"""
import io
import re

import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
HEADERS = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}


async def _get(url: str) -> str:
    async with httpx.AsyncClient(
        headers=HEADERS, follow_redirects=True, timeout=30
    ) as http:
        resp = await http.get(url)
        resp.raise_for_status()
        return resp.text


async def fetch_scholar_profile(url: str) -> dict:
    """Parse a public Google Scholar profile: author, affiliation, metrics,
    and up to 100 publications with citation counts."""
    sep = "&" if "?" in url else "?"
    html = await _get(f"{url}{sep}pagesize=100")
    soup = BeautifulSoup(html, "lxml")

    name = soup.select_one("#gsc_prf_in")
    affiliation = soup.select_one(".gsc_prf_il")
    interests = [a.get_text(strip=True) for a in soup.select("#gsc_prf_int a")]

    metrics: dict = {}
    table = soup.select_one("#gsc_rsb_st")
    if table:
        rows = table.select("tbody tr")
        labels = ["citations", "h_index", "i10_index"]
        for label, row in zip(labels, rows):
            cells = [c.get_text(strip=True) for c in row.select("td")]
            if len(cells) >= 2:
                metrics[label] = _to_int(cells[1])
                if len(cells) >= 3:
                    metrics[f"{label}_recent"] = _to_int(cells[2])

    publications = []
    for tr in soup.select("#gsc_a_b .gsc_a_tr"):
        title_el = tr.select_one(".gsc_a_at")
        gray = tr.select(".gs_gray")
        cited = tr.select_one(".gsc_a_ac")
        year = tr.select_one(".gsc_a_y")
        publications.append(
            {
                "title": title_el.get_text(strip=True) if title_el else "",
                "authors": gray[0].get_text(strip=True) if len(gray) > 0 else "",
                "venue": gray[1].get_text(strip=True) if len(gray) > 1 else "",
                "cited_by": _to_int(cited.get_text(strip=True)) if cited else 0,
                "year": _to_int(year.get_text(strip=True)) if year else None,
            }
        )

    return {
        "source": "google_scholar",
        "url": url,
        "name": name.get_text(strip=True) if name else None,
        "affiliation": affiliation.get_text(strip=True) if affiliation else None,
        "interests": interests,
        "metrics": metrics,
        "publications": publications,
    }


async def fetch_homepage(url: str) -> dict:
    """Fetch a personal homepage and reduce it to readable text."""
    html = await _get(url)
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "noscript"]):
        tag.decompose()
    text = re.sub(r"\n{3,}", "\n\n", soup.get_text("\n", strip=True))
    return {"source": "homepage", "url": url, "text": text[:20000]}


def extract_pdf_text(content: bytes, max_chars: int = 40000) -> str:
    reader = PdfReader(io.BytesIO(content))
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
        if sum(len(p) for p in parts) > max_chars:
            break
    return "\n".join(parts)[:max_chars]


def _to_int(s: str | None) -> int | None:
    if not s:
        return None
    digits = re.sub(r"[^\d]", "", s)
    return int(digits) if digits else None
