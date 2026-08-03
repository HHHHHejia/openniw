#!/usr/bin/env python3
"""Export the de-identified benchmark dataset from the public_source case DB.

Reads the local case_source.db (NOT in this repo) and writes a compact,
fully de-identified columnar JSON to frontend/public/benchmark-data.json:
per approved case only [month-index, category, field-group, citations,
publications]. No names, no URLs, no narratives — nothing traceable.

Usage:  python3 scripts/export_benchmark.py [path/to/case_source.db]
"""
import json
import pathlib
import sqlite3
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[1]
OUT = REPO / "frontend" / "public" / "benchmark-data.json"
DEFAULT_DB = REPO.parent / "case_source_db" / "case_source.db"

YM0 = (2012, 1)  # month index 0 = 2012-01

# Keyword rules, first match wins (checked lowercased). Order matters:
# specific before general.
FIELD_GROUPS: list[tuple[str, list[str]]] = [
    ("Computer Science & AI",
     ["machine learning", "artificial intelligence", "deep learning",
      "computer", "software", "data science", "data mining", "nlp",
      "computer vision", "cybersecurity", "informatics", "robotics",
      "human-computer"]),
    ("Electrical & Electronics Eng.",
     ["electrical", "electronic", "semiconductor", "photonics", "optics",
      "signal processing", "telecommunication", "wireless", "circuit",
      "microelectronic", "embedded"]),
    ("Mechanical & Aerospace Eng.",
     ["mechanical", "aerospace", "aeronautic", "automotive", "manufacturing",
      "thermal", "fluid", "robotic engineering", "mechatronic"]),
    ("Civil & Environmental Eng.",
     ["civil", "structural engineering", "construction", "transportation",
      "geotechnical", "environmental engineering", "water resource",
      "urban planning", "architecture"]),
    ("Materials Science",
     ["materials", "material science", "polymer", "nanotechnology", "nano",
      "metallurgy", "coating", "composite"]),
    ("Chemistry & Chemical Eng.",
     ["chemistry", "chemical", "catalysis", "electrochem", "petroleum",
      "petrochemical"]),
    ("Energy & Sustainability",
     ["energy", "battery", "solar", "renewable", "power system", "nuclear",
      "sustainab", "climate", "carbon"]),
    ("Life Sciences",
     ["biology", "biolog", "genetic", "genomic", "neurosci", "microbio",
      "biochem", "molecular", "cell", "immunolog", "biotechnolog",
      "bioinformatic", "ecolog", "plant", "agricultur", "food science",
      "veterinar", "zoolog", "marine"]),
    ("Medicine & Health",
     ["cancer", "oncolog", "medicine", "medical", "clinical", "health",
      "pharma", "drug", "epidemiolog", "public health", "surgery",
      "cardio", "radiol", "patholog", "dentist", "nursing", "psychiatr",
      "therap", "disease", "biomedical"]),
    ("Physics & Astronomy",
     ["physics", "astronom", "astrophys", "quantum", "particle"]),
    ("Math & Statistics",
     ["mathematic", "statistic", "operations research", "optimization"]),
    ("Earth & Geosciences",
     ["geolog", "geophys", "geoscien", "atmospher", "meteorolog",
      "oceanograph", "hydrolog", "seismolog", "remote sensing"]),
    ("Business, Economics & Finance",
     ["business", "economic", "finance", "financial", "management",
      "marketing", "accounting", "supply chain", "entrepreneur"]),
    ("Social Sciences & Humanities",
     ["psycholog", "sociolog", "education", "linguist", "political",
      "law", "policy", "anthropolog", "history", "communication",
      "journalism", "philosoph"]),
    ("Arts, Design & Sports",
     ["art", "music", "design", "film", "fashion", "sport", "athlet",
      "coach", "dance", "photograph"]),
]


def field_group(raw: str | None) -> str:
    low = (raw or "").lower()
    for name, kws in FIELD_GROUPS:
        if any(kw in low for kw in kws):
            return name
    return "Other fields"


def ym_index(iso_date: str) -> int | None:
    try:
        y, m = int(iso_date[:4]), int(iso_date[5:7])
    except (TypeError, ValueError):
        return None
    return (y - YM0[0]) * 12 + (m - YM0[1])


def main() -> int:
    db_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DB
    if not db_path.exists():
        print(f"DB not found: {db_path}", file=sys.stderr)
        return 1
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    rows = con.execute(
        """SELECT approval_date, category, general_field,
                  citations_count, publications_count,
                  processing_days, premium_processing
           FROM cases
           WHERE approval_date IS NOT NULL
             AND citations_count IS NOT NULL
             AND needs_review = 0""").fetchall()

    # --- precomputed aggregates for the insight cards / weekly pulse -----
    def one(sql: str):
        return con.execute(sql).fetchone()

    rec_rows = con.execute(
        """SELECT rec_letters_count, COUNT(*) FROM cases
           WHERE category='NIW' AND rec_letters_count IS NOT NULL
           GROUP BY 1 ORDER BY 1""").fetchall()
    rec_hist = {str(min(int(k), 10)): 0 for k, _ in rec_rows}
    for k, n in rec_rows:
        rec_hist[str(min(int(k), 10))] = rec_hist.get(str(min(int(k), 10)), 0) + n
    rfe = one("""SELECT ROUND(100.0*SUM(rfe='received_overcome')
                        / SUM(rfe IN ('none','received_overcome')), 1),
                        SUM(rfe IN ('none','received_overcome'))
                 FROM cases WHERE category='NIW' AND approval_date>='2024'""")
    weekly = con.execute(
        """SELECT week_start, total_approvals, niw_count, niw_cite_med
           FROM weekly_stats WHERE week_start IS NOT NULL
           ORDER BY week_start DESC LIMIT 12""").fetchall()
    con.close()

    groups = [name for name, _ in FIELD_GROUPS] + ["Other fields"]
    g_idx = {g: i for i, g in enumerate(groups)}
    categories: list[str] = []
    cases = []
    PREMIUM = {"yes": 1, "upfront": 1, "upgrade": 2}
    for date, cat, field, cites, pubs, pdays, prem in rows:
        ym = ym_index(date)
        if ym is None or ym < 0:
            continue
        if cat not in categories:
            categories.append(cat)
        cases.append([ym, categories.index(cat), g_idx[field_group(field)],
                      int(cites), int(pubs) if pubs is not None else -1,
                      int(pdays) if pdays is not None else -1,
                      PREMIUM.get(prem, 0)])

    cases.sort()
    out = {
        "generated": time.strftime("%Y-%m-%d"),
        "source": ("Aggregated from publicly posted I-140 approval notices "
                   "(public-approval-source), 2012-2026. Approved cases only - "
                   "survivor-biased by construction."),
        "ym0": f"{YM0[0]}-{YM0[1]:02d}",
        "categories": categories,
        "fields": groups,
        "columns": ["ym", "category", "field", "citations", "publications",
                    "processing_days", "premium"],
        "premium_codes": {"0": "none or undisclosed", "1": "premium",
                          "2": "mid-case upgrade"},
        "aggregates": {
            "rec_letters_niw_hist": rec_hist,
            "rfe_overcome_2024": {"rate": rfe[0], "n": rfe[1]},
            "weekly": [[w, t, n, m] for w, t, n, m in weekly],
        },
        "cases": cases,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(out, separators=(",", ":"))
    OUT.write_text(payload)
    web_out = REPO / "webpage" / "public" / "benchmark-data.json"
    if web_out.parent.is_dir():
        web_out.write_text(payload)  # keep the public site's copy in sync
    # report
    from collections import Counter
    per_group = Counter(groups[c[2]] for c in cases)
    print(f"{len(cases)} cases -> {OUT} "
          f"({OUT.stat().st_size // 1024} KB)")
    for g, n in per_group.most_common():
        print(f"  {n:5d}  {g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
