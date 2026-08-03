#!/usr/bin/env python3
"""Batch-download the applicant's own publications (stdlib only).

Resolves each title on OpenAlex, follows the best open-access location
(arXiv, PubMed Central, publisher OA), downloads PDFs into sources/papers/
and writes a provenance manifest. Preprint-only and undownloadable rows are
reported so the agent can ask the user to supply the published PDFs.

Usage:
    python3 fetch_papers.py "Title 1" "Title 2" ... [--out sources/papers]
"""
import json
import pathlib
import re
import sys
import time
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from harvest_citations import _get, title_sim  # noqa: E402

UA = {"User-Agent": (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")}

# --- BEGIN SYNC: paper download (source of truth: src/openniw/services/papers.py) ---
def _slug(title: str, year) -> str:
    words = re.sub(r"[^a-z0-9 ]", "", (title or "paper").lower()).split()[:6]
    return f"{year or 'nd'}-{'-'.join(words) or 'paper'}"


def _oa_candidates(work: dict) -> list[dict]:
    """OA locations, best first: published > accepted > submitted version."""
    locs = []
    best = work.get("best_oa_location") or {}
    if best.get("pdf_url"):
        locs.append(best)
    for loc in work.get("locations") or []:
        if loc.get("pdf_url") and loc.get("pdf_url") != best.get("pdf_url"):
            locs.append(loc)
    rank = {"publishedVersion": 0, "acceptedVersion": 1, "submittedVersion": 2}
    locs.sort(key=lambda l: rank.get(l.get("version"), 3))
    return locs


def _download_pdf(url: str, dest: pathlib.Path) -> bool:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = resp.read()
        if not data.startswith(b"%PDF"):
            return False
        dest.write_bytes(data)
        return True
    except Exception:
        return False


def download_papers(titles: list[str], out_dir: pathlib.Path,
                    log=print) -> dict:
    """Download OA PDFs for the applicant's papers into out_dir.

    Writes out_dir/manifest.json; returns a summary dict. Idempotent:
    titles already downloaded (per manifest) are skipped.
    """
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "manifest.json"
    manifest: list[dict] = []
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
        except Exception:
            manifest = []
    done_titles = {r["query_title"] for r in manifest
                   if r.get("status") == "downloaded"}

    def _flush() -> None:
        manifest_path.write_text(
            json.dumps(manifest, indent=1, ensure_ascii=False))

    for title in titles:
        if title in done_titles:
            log(f"  already downloaded: {title[:60]}")
            continue
        row = {"query_title": title, "status": "unresolved",
               "fetched_at": time.strftime("%Y-%m-%d")}
        manifest = [r for r in manifest if r["query_title"] != title]
        manifest.append(row)
        try:
            data = _get("/works", search=title[:250], **{"per-page": 1})
        except Exception as exc:
            row["status"], row["error"] = "network_error", str(exc)
            _flush()
            log(f"  NETWORK ERROR: {title[:60]}")
            continue
        results = data.get("results") or []
        if not results or title_sim(
                title, results[0].get("display_name") or "") < 0.55:
            _flush()
            log(f"  NOT RESOLVED on OpenAlex: {title[:70]}")
            continue
        w = results[0]
        row.update({
            "resolved_title": w.get("display_name"),
            "doi": w.get("doi"),
            "year": w.get("publication_year"),
            "venue": ((w.get("primary_location") or {}).get("source")
                      or {}).get("display_name"),
        })
        candidates = _oa_candidates(w)
        if not candidates:
            row["status"] = "no_oa_pdf"
            _flush()
            log(f"  no OA PDF (user must supply published version): "
                f"{title[:60]}")
            continue
        fname = _slug(w.get("display_name"), w.get("publication_year")) + ".pdf"
        saved = False
        for loc in candidates:
            if _download_pdf(loc["pdf_url"], out_dir / fname):
                row.update({
                    "status": "downloaded",
                    "file": fname,
                    "oa_version": loc.get("version"),
                    "source_url": loc.get("pdf_url"),
                    "preprint_only":
                        loc.get("version") != "publishedVersion",
                })
                saved = True
                break
            time.sleep(0.5)
        if not saved:
            row["status"] = "download_failed"
            row["tried_urls"] = [l.get("pdf_url") for l in candidates[:3]]
        _flush()
        log(f"  {'saved ' + fname if saved else 'DOWNLOAD FAILED'}: "
            f"{title[:55]}")
        time.sleep(0.3)

    _flush()
    by = lambda s: sum(1 for r in manifest if r.get("status") == s)
    summary = {
        "requested": len(titles),
        "downloaded": by("downloaded"),
        "preprint_only": sum(1 for r in manifest
                             if r.get("preprint_only")),
        "no_oa_pdf": by("no_oa_pdf"),
        "unresolved": by("unresolved"),
        "failed": by("download_failed") + by("network_error"),
        "manifest": str(manifest_path),
    }
    return summary
# --- END SYNC: paper download ---


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(
        description="Batch-download the applicant's own papers (OA PDFs)")
    ap.add_argument("titles", nargs="+", help="the applicant's paper titles")
    ap.add_argument("--out", default="sources/papers")
    ns = ap.parse_args()
    summary = download_papers(ns.titles, pathlib.Path(ns.out))  # noqa: F821
    print(json.dumps(summary, ensure_ascii=False))
    if summary["preprint_only"]:
        print(f"NOTE: {summary['preprint_only']} paper(s) only available as "
              "preprints — the published version is the preferred exhibit; "
              "ask the user to supply it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
