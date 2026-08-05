#!/usr/bin/env python3
"""Export the de-identified benchmark dataset from a local case database.

Reads a local SQLite database (NOT in this repo) and writes a compact,
fully de-identified columnar JSON to frontend/public/benchmark-data.json:
per approved case only [month-index, category, field-group, citations,
publications]. No names, no URLs, no narratives — nothing traceable.

Usage:  python3 scripts/export_benchmark.py [path/to/cases.db]
"""
import json
import os
import pathlib
import re
import sqlite3
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[1]
OUT = REPO / "frontend" / "public" / "benchmark-data.json"
# The source database is the maintainer's own collection of publicly posted
# approval notices. It is not in this repository and is not distributed:
# only the aggregate above ships. Pass a path as argv[1], or set
# OPENNIW_CASE_DB.
DEFAULT_DB = pathlib.Path(
    os.environ.get("OPENNIW_CASE_DB") or REPO.parent / "case-db" / "cases.db")

YM0 = (2012, 1)  # month index 0 = 2012-01

# --- Coarsening ------------------------------------------------------------
# Every value here also appears on the public notice it came from, so an exact
# figure is a join key: before coarsening, 86.6% of rows were unique on
# (month, category, field, citations) alone, and citations + processing_days
# together pinned a case to a specific filing. Values are therefore released
# at the resolution the charts actually use — quantiles and buckets — and no
# finer. Measured cost: every published percentile moves by at most 4.5%, and
# publications percentiles do not move at all.


def _round_to(value: int, step: int) -> int:
    return int(round(value / step) * step)


def coarsen_citations(c: int) -> int:
    """Widening buckets: precision matters least where the tail is thinnest,
    and the extreme tail identifies a person on its own, so it is capped."""
    if c < 0:
        return c
    if c >= 2000:
        return 2000          # above the 98th percentile; the charts top out lower
    if c >= 1000:
        return _round_to(c, 100)
    if c >= 500:
        return _round_to(c, 50)
    if c >= 200:
        return _round_to(c, 25)
    if c >= 50:
        return _round_to(c, 10)
    return _round_to(c, 5)


def coarsen_publications(p: int) -> int:
    """Left alone below 20 — the values are small and collide heavily on their
    own, and coarsening there would move the low percentiles for no gain."""
    if p < 0:
        return p
    if p >= 150:
        return 150
    if p >= 50:
        return _round_to(p, 10)
    if p >= 20:
        return _round_to(p, 2)
    return p


def coarsen_days(d: int) -> int:
    """Weeks, not days: a day-exact pendency plus the approval month names the
    filing date."""
    if d < 0:
        return d
    if d >= 730:
        return 730
    return max(7, _round_to(d, 7))



# Regex rules over normalized field names. First match wins, so broad patterns
# come only after domain-specific ones. Word boundaries are intentional: the
# old substring rule classified "Earth Science" as art because "earth"
# contains "art", and treated every engineering use of "design" as art.
FIELD_GROUPS: list[tuple[str, tuple[str, ...]]] = [
    ("Computer Science & AI", (
        r"\b(?:artificial intelligence|machine learning|deep learning|"
        r"reinforcement learning|multimodal learning|robot learning)\b",
        r"\b(?:ai|nlp)\b", r"\blarge language models?\b",
        r"\b(?:computer|computing|software|informatics?)\b",
        r"\bcomputational (?:science|engineering|modeling|analysis|"
        r"intelligence)\b",
        r"\bdata (?:science|mining|engineering|analytics?|processing|"
        r"analysis|security|privacy)\b",
        r"\b(?:information technology|information systems?|information "
        r"sciences?|information studies|information security|"
        r"information theory)\b",
        r"\b(?:cyber ?security|it security|digital forensics|cryptograph\w*|"
        r"blockchain|programming languages?)\b",
        r"\b(?:natural language processing|language technolog\w*|computer "
        r"vision|visual computing|scientific visualization)\b",
        r"\b(?:robot\w*|human (?:computer|machine|robot) interaction|"
        r"human centered research and design)\b",
        r"\b(?:autonomous|intelligent|connected|cyber physical|networked?) "
        r"systems?\b",
        r"\b(?:complex networks?|network science|digitization|"
        r"supercomputing|high performance computing)\b",
        r"\b(?:neural networks?|network engineering|machine vision|"
        r"manifold learning|internet communications?)\b",
        r"\binformation and communications technology\b",
        r"\b(?:mobile networks?|systems security|knowledge representation "
        r"and reasoning|complex system modeling|autonomous driving|"
        r"autonomous vehicles?|human centric perception)\b",
        r"\b(?:biocomputing|image video compression|privacy preserving "
        r"advertisement measurement)\b",
        r"^information$",
    )),
    ("Electrical & Electronics Eng.", (
        r"\b(?:electrical|electronic|semiconductor|microelectronic|"
        r"embedded)\w*\b",
        r"\b(?:photonics?|plasmonics?|optics?|optical|laser)\b",
        r"\b(?:signal processing|speech processing|telecommunications?|"
        r"wireless|circuits?)\b",
        r"\b(?:electromagnetic|microwave|radio ?frequency|radiofrequency|"
        r"antenna)\w*\b",
        r"\b(?:sensors?|sensing|biosensors?|instrumentation|"
        r"device engineering|imaging device)\b",
        r"\b(?:electric power|power electric|power engineering)\b",
        r"\b(?:control systems?|control engineering|control science|"
        r"systems control engineering|dynamic system control)\b",
        r"\b(?:microsystems?|micro systems) engineering\b",
        r"\b(?:hardware designs?|human machine interfaces?)\b",
        r"\b(?:optoelectronic\w*|biophotonics?|nanophotonics?|"
        r"microelectromechanical systems?|neural engineering|automation|"
        r"novel devices?)\b",
        r"\b(?:neuroengineering|nanoelectronics|bioelectronics engineering|"
        r"microscopy|imaging sciences?|computational imaging|"
        r"super resolution imaging|metrology|lighting research)\b",
        r"\bmicro electromechanical systems?\b",
    )),
    ("Mechanical & Aerospace Eng.", (
        r"\b(?:mechanical|mechanics|mechanism design|mechatronic|"
        r"biomech\w*)\b",
        r"\b(?:mechatronics?|nanomechanics|neuromechanics)\b",
        r"\b(?:systems? design(?: engineering)?|space technologies and "
        r"systems|robust control of diesel drivelines)\b",
        r"\b(?:aerospace|aeronautic|space engineering|unmanned aerial "
        r"vehicles?)\b",
        r"\baeronautics engineering\b",
        r"\b(?:automotive|vehicles?|driveline|manufacturing|industrial "
        r"engineering|production engineering)\b",
        r"\b(?:thermal|thermodynamics|heat transfer|fluid|combustion|hvac)\b",
        r"\b(?:welding|machining|precision engineering|ocean engineering|"
        r"acoustics|microfluidics|micro scale engineering|"
        r"aftertreatment technologies)\b",
        r"\b(?:solid mechanics|damage mechanics|engineering mechanics|"
        r"systems engineering)\b",
    )),
    ("Civil & Environmental Eng.", (
        r"\b(?:civil|structural|construction|transportation|traffic|"
        r"geotechnical|pavement)\w*\b",
        r"\b(?:environmental engineering|architectural engineering|"
        r"architecture|urban (?:planning|design)|city planning)\b",
        r"\b(?:infrastructure|bridge engineering|dam engineering|"
        r"hydraulic structures?|coastal engineering)\b",
        r"\b(?:water resources?|water quality engineering|water treatment|"
        r"building (?:science|technology)|geomechanics)\b",
    )),
    ("Materials Science", (
        r"\b(?:materials?|material science|polymers?|nanotechnolog\w*|"
        r"nanomaterials?|metallurg\w*|coatings?|composites?)\b",
        r"\b(?:corrosion|surface science|rheology|crystal engineering|"
        r"membrane science|plastics engineering)\b",
        r"\b(?:nanoscience|nanoengineering|nanoscale engineering|"
        r"biomaterials?|metamaterials?|nanocomposite\w*)\b",
        r"\b(?:nano science|nanofabrication)\b",
        r"\b(?:textiles?|packaging science|paper and printing science|"
        r"wood science|electroceramics|superconductors?)\b",
    )),
    ("Chemistry & Chemical Eng.", (
        r"\b(?:chemistry|chemical|catalysis|electrochem\w*|petroleum|"
        r"petrochemical)\b",
        r"\b(?:organic synthesis|spectroscopy|glycoscience|"
        r"bioanalytical science|process engineering|radiochemistry|"
        r"photochemistry|macromolecular engineering)\b",
        r"\b(?:nanochemistry|cosmochemistry)\b",
    )),
    ("Energy & Sustainability", (
        r"\b(?:energy|batter(?:y|ies)|solar|renewable|photovoltaics?|"
        r"nuclear|sustainab\w*|carbon)\b",
        r"\b(?:power systems?|biofuels?|biogas|alternative fuels?|"
        r"fuel research)\b",
        r"\b(?:bioenergy|biorenewable|geothermal|reservoir engineering)\b",
    )),
    ("Medicine & Health", (
        r"\b(?:medicine|medical|clinical|health|biomedical|pharma\w*|"
        r"drugs?|epidemiolog\w*|public health|healthcare|biomedicine|"
        r"nanomedicine)\b",
        r"\b(?:cancer|oncolog\w*|surgery|surgical|therap\w*|diseases?|"
        r"disorders?|patholog\w*|nursing)\b",
        r"\b(?:cardi\w*|radiolog\w*|psychiatr\w*|gastro\w*|hepat\w*|"
        r"neurolog\w*|neuroimaging|neurosurg\w*|neuroradiolog\w*|"
        r"neurodegeneration)\b",
        r"\b(?:nephrolog\w*|renal|ophthalmolog\w*|endocrinolog\w*|"
        r"urolog\w*|dermatolog\w*|hematolog\w*|anesthesiolog\w*)\b",
        r"\b(?:pediatrics?|pulmonolog\w*|rheumatolog\w*|critical care|"
        r"rehabilitation|orthoped\w*|optometry|gerontolog\w*|aging)\b",
        r"\b(?:otolaryngolog\w*|gynecolog\w*|obstetrics?|transplantation|"
        r"pathophysiolog\w*|pharmacolog\w*|immunotherap\w*)\b",
        r"\b(?:dent\w*|stomatolog\w*|orthodont\w*|periodont\w*|"
        r"endodont\w*|orofacial)\b",
        r"\b(?:dementia|epilepsy|diabetes|thrombotic|vascular neurology|"
        r"substance use|hearing science|vision science)\b",
        r"\b(?:nutrition\w*|kinesiology|movement science|exercise physiology)\b",
        r"\b(?:vaccine development|biotherapeutics?|translational research|"
        r"diagnostic biomarkers?|magnetic resonance imaging)\b",
        r"\b(?:neuro\w*pharmacolog\w*|biopharmaceutical sciences?|"
        r"ethnomedicine|psychotherapy|neuromodulation|vestibular research|"
        r"perioperative outcomes research|hematopathology)\b",
        r"\btranslational science\b",
    )),
    ("Life Sciences", (
        r"\b(?:biology|biological|biosciences?|life sciences?|genetics?|"
        r"genomics?|neurosciences?|neurobiology|pathobiology|microbiolog\w*|"
        r"virolog\w*)\b",
        r"\b(?:biochem\w*|molecular|cells?|immunolog\w*|biotechnolog\w*|"
        r"bioinformatic\w*|bioengineering|biosystems engineering)\b",
        r"\b(?:physiology|toxicolog\w*|proteomics?|metabolomics?|"
        r"metabolism|anatom\w*|tissue engineering|biophysics|"
        r"neurophysiology|neuroimmunology)\b",
        r"\b(?:immunobiology|bionanotechnology|nanobiotechnology|"
        r"neurometabolism|neuroproteomics|neurotoxicity|neurogenetics|"
        r"neurodevelopment|chronobiology)\b",
        r"\b(?:ecolog\w*|plants?|agricultur\w*|food (?:science|safety|"
        r"technology|engineering)|veterinar\w*|zoolog\w*|marine)\b",
        r"\b(?:agronomy|soil science|animal sciences?|botany|entomolog\w*|"
        r"forestry|aquaculture|crop science|horticultur\w*|poultry|dairy)\b",
        r"\b(?:pest control|weed science|olericulture|enology|"
        r"reproductive science|protein science|bioprocess engineering|"
        r"epigenetics|ecosystem science|bioresource science)\b",
        r"\b(?:botanical|herbal science|biomolecular engineering|"
        r"metabolic engineering|antibody engineering|parasitology|"
        r"animal reproduction)\b",
        r"\b(?:computational multiomics|biopharmacognosy|protein aggregation)\b",
    )),
    ("Physics & Astronomy", (
        r"\b(?:physics|physicist|physical science|astronom\w*|astrophys\w*|"
        r"quantum|particle)\b",
        r"\b(?:cosmology|condensed matter|magnetism|superconductivity|"
        r"space science)\b",
        r"\b(?:nanophysics|physical modeling)\b",
    )),
    ("Math & Statistics", (
        r"\b(?:mathematics?|statistics?|biostatistics?|operations research|"
        r"optimization)\b",
        r"\b(?:quantitative methods?|graph theory|number theory|algebraic|"
        r"topology|dynamical systems?|numerical modeling|mathematical "
        r"modeling|statistical modeling|biostatics)\b",
        r"\b(?:quantitative analysis|statistical science|senior statistician|"
        r"computational and mathematical engineering)\b",
    )),
    ("Earth & Geosciences", (
        r"\b(?:earth sciences?|geolog\w*|geophys\w*|geoscien\w*|"
        r"geograph\w*|geospatial|gis)\b",
        r"\b(?:atmospher\w*|meteorolog\w*|oceanograph\w*|hydrolog\w*|"
        r"seismolog\w*|remote sensing|planetary sciences?|geospace)\b",
        r"\b(?:environmental sciences?|climatolog\w*|air (?:pollution|"
        r"quality)|natural resources?|watershed science|conservation science)\b",
        r"\b(?:mineral processing|aerosol science|soil and crop sciences?)\b",
        r"\b(?:geoinformatics|geochemistry|climate science|hydrogeolog\w*|"
        r"earth system modeling|hydrometeorolog\w*|agrometeorolog\w*|"
        r"environmental analysis)\b",
        r"\b(?:paleoclimatolog\w*|biogeochemistry|groundwater resources?|"
        r"crop and soil sciences?|geo and cosmochemistry)\b",
        r"\bseismic and uncertainty analysis\b",
    )),
    ("Business, Economics & Finance", (
        r"\b(?:business|econom\w*|finance|financial|management|marketing|"
        r"accounting|supply chain|entrepreneur\w*)\b",
        r"\b(?:organizational behavior|human resources?|digital economy|"
        r"corporate governance|technology strategy|risk governance)\b",
        r"\bapplied microeconom(?:ics|etrics)\b",
    )),
    ("Social Sciences & Humanities", (
        r"\b(?:psycholog\w*|sociolog\w*|education|learning sciences?|"
        r"linguist\w*|language teaching)\b",
        r"\b(?:political|law|policy|anthropolog\w*|history|communication|"
        r"journalism|philosoph\w*)\b",
        r"\b(?:social sciences?|social work|social welfare|criminolog\w*|"
        r"public administration|international development)\b",
        r"\b(?:family studies|human development|behavioral sciences?|"
        r"behavioral addictions|jewish studies|english|cognitive science|"
        r"educational technology)\b",
        r"\b(?:neuroeducation|educational leadership)\b",
        r"\b(?:land governance|psychometrics|computational social science)\b",
    )),
    ("Arts, Design & Sports", (
        r"\b(?:arts?|music|film|fashion|sports?|athletics?|coach\w*|dance|"
        r"photograph\w*)\b",
        r"\b(?:graphic design|visual design|industrial design|apparel)\b",
        r"\bdesign(?: science)?\b",
    )),
]

_FIELD_GROUP_PATTERNS = [
    (name, tuple(re.compile(pattern) for pattern in patterns))
    for name, patterns in FIELD_GROUPS
]


def field_group(raw: str | None) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", (raw or "").casefold()).strip()
    for name, patterns in _FIELD_GROUP_PATTERNS:
        if any(pattern.search(normalized) for pattern in patterns):
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
        if cat == "O1A":  # merge into one O-1 pool for the UI
            cat = "O1"
        if cat not in categories:
            categories.append(cat)
        cases.append([ym, categories.index(cat), g_idx[field_group(field)],
                      coarsen_citations(int(cites)),
                      coarsen_publications(int(pubs)) if pubs is not None else -1,
                      coarsen_days(int(pdays)) if pdays is not None else -1,
                      PREMIUM.get(prem, 0)])

    cases.sort()
    out = {
        "generated": time.strftime("%Y-%m-%d"),
        "source": ("Aggregated from publicly posted I-140 and O-1 approval "
                   "notices, 2012-2026. Approved cases only - "
                   "survivor-biased by construction. Dates are month-only; "
                   "citations, publications and pendency are released in "
                   "buckets, not exact figures."),
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
