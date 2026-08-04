"""Lint documents/source-registry.md — the claim → evidence table.

The registry is a printable markdown file the agent maintains WHILE
drafting: every factual claim gets a row, and load-bearing claims (what the
petition letter argues from, third-party entities, impact assertions) also
carry a locator, an independent verifier, a measure and a gap.

This module is the deterministic half. It never writes and never judges the
merits — it reports rows that cannot support the weight put on them:
missing sources, missing independent verifiers, dead exhibit references, and
cells filled with placeholder text, which is how a verification table
becomes theatre.

Format contract (two tables, tier by heading — no new syntax):

    ## Load-bearing claims
    | claim | source | locator | independent verifier | measure | gap |
    |---|---|---|---|---|---|
    | ... | Ex. 12 | Ex. 12 at 3, ¶2 | Prof. X (no shared work) | 41% | |

    ## Supporting facts
    | claim | source |
    |---|---|
    | ... | Ex. 4 |
"""
from __future__ import annotations

import dataclasses
import pathlib
import re

LOAD_BEARING = "load-bearing"
SUPPORTING = "supporting"

# Column keys, in order. Headers are matched loosely (case- and
# punctuation-insensitive) so an author may write "Independent verifier".
FULL_COLUMNS = ["claim", "source", "locator", "independent verifier",
                "measure", "gap"]
LIGHT_COLUMNS = ["claim", "source"]

# A cell holding one of these is empty in every sense that matters. This is
# the check that separates a real registry from a filled-in-looking one.
FILLER = {
    "", "-", "--", "—", "–", "n/a", "na", "n.a.", "none given", "tbd", "tba",
    "todo", "?", "??", "unknown", "pending", "see above", "same as above",
    "ditto", "as above", "idem", "same", "see below", "various", "multiple",
    "TBD.", "x",
}

# "NONE — self-serving" is a deliberate, honest answer, not a filler: the
# claim has no independent verifier and the author has said so. It needs a
# decision (obtain an attestation, or cut the claim), not a correction.
SELF_SERVING = re.compile(r"^\s*none\b", re.I)

_EXHIBIT = re.compile(r"\bexhibits?\.?\s*(\d+)\s*(?:[–—-]\s*(\d+))?", re.I)
_EX_SHORT = re.compile(r"\bex\.\s*(\d+)\s*(?:[–—-]\s*(\d+))?", re.I)
_URL = re.compile(r"https?://")


@dataclasses.dataclass
class Row:
    tier: str
    line: int
    cells: dict[str, str]

    @property
    def claim(self) -> str:
        return self.cells.get("claim", "")


@dataclasses.dataclass
class Finding:
    severity: str   # "error" | "warn" | "decide"
    line: int
    claim: str
    message: str

    def as_dict(self) -> dict:
        return dataclasses.asdict(self)


def _norm_header(cell: str) -> str:
    return re.sub(r"[^a-z ]", "", cell.strip().lower()).strip()


def _split_row(line: str) -> list[str]:
    """Split a markdown table row, honouring \\| escapes inside cells."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    parts = re.split(r"(?<!\\)\|", body)
    return [p.replace(r"\|", "|").strip() for p in parts]


def _is_divider(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c)


def parse(text: str) -> tuple[list[Row], list[Finding]]:
    """Parse the registry into rows. Structural problems become findings."""
    rows: list[Row] = []
    findings: list[Finding] = []
    tier = SUPPORTING          # rows before any heading are treated as light
    columns: list[str] | None = None

    for n, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip()
        heading = re.match(r"^#{1,6}\s+(.*)", line)
        if heading:
            title = heading.group(1).lower()
            if "load" in title or "load-bearing" in title:
                tier = LOAD_BEARING
            elif "support" in title:
                tier = SUPPORTING
            columns = None      # a heading always ends the previous table
            continue
        if not line.strip().startswith("|"):
            continue

        cells = _split_row(line)
        if _is_divider(cells):
            continue
        if columns is None:     # first table line after a heading = header
            columns = [_norm_header(c) for c in cells]
            expected = FULL_COLUMNS if tier == LOAD_BEARING else LIGHT_COLUMNS
            if columns[:len(expected)] != expected:
                findings.append(Finding(
                    "error", n, "",
                    f"{tier} table header is {columns!r}; expected "
                    f"{expected!r} (extra trailing columns are allowed)"))
            continue

        if len(cells) < len(columns):
            cells += [""] * (len(columns) - len(cells))
        rows.append(Row(tier, n, dict(zip(columns, cells))))

    return rows, findings


def _blank(value: str) -> bool:
    return value.strip().lower() in FILLER


def _exhibit_numbers(text: str) -> set[int]:
    found: set[int] = set()
    for rx in (_EXHIBIT, _EX_SHORT):
        for m in rx.finditer(text):
            lo = int(m.group(1))
            hi = int(m.group(2)) if m.group(2) else lo
            if hi >= lo and hi - lo < 200:
                found.update(range(lo, hi + 1))
    return found


def known_exhibits(index_text: str) -> set[int]:
    """Exhibit numbers declared in documents/exhibit-index.md."""
    numbers = {int(m) for m in re.findall(r"^\s*(\d{1,3})[.)]\s", index_text,
                                          re.M)}
    numbers |= _exhibit_numbers(index_text)
    return numbers


def check(rows: list[Row], exhibits: set[int] | None = None) -> list[Finding]:
    findings: list[Finding] = []
    seen: dict[str, int] = {}

    for row in rows:
        claim = row.claim
        short = (claim[:60] + "…") if len(claim) > 60 else claim
        if _blank(claim):
            findings.append(Finding("error", row.line, short,
                                    "row has no claim text"))
            continue

        key = re.sub(r"\W+", " ", claim.lower()).strip()
        if key in seen:
            findings.append(Finding(
                "warn", row.line, short,
                f"same claim already on line {seen[key]} — if the two rows "
                "cite different numbers or dates, that is a contradiction"))
        else:
            seen[key] = row.line

        source = row.cells.get("source", "")
        if _blank(source):
            findings.append(Finding("error", row.line, short,
                                    "no source — every claim binds to an "
                                    "exhibit or a URL + quote, or it comes out"))
        elif _URL.search(source) and not re.search(r"\d{4}", source):
            findings.append(Finding("warn", row.line, short,
                                    "web source without a retrieval date"))

        if row.tier != LOAD_BEARING:
            continue

        verifier = row.cells.get("independent verifier", "")
        if _blank(verifier):
            findings.append(Finding(
                "error", row.line, short,
                "load-bearing claim with no independent verifier — name one, "
                'or write "NONE — self-serving" if that is the truth'))
        elif SELF_SERVING.match(verifier):
            findings.append(Finding(
                "decide", row.line, short,
                "no independent verifier: obtain an attestation from someone "
                "with no stake in the outcome, or cut the claim"))

        if _blank(row.cells.get("locator", "")):
            findings.append(Finding(
                "warn", row.line, short,
                "no page/paragraph locator — an officer who cannot find the "
                "proof has not been given it"))

        gap = row.cells.get("gap", "")
        if not _blank(gap):
            findings.append(Finding("warn", row.line, short,
                                    f"open gap: {gap}"))

        if exhibits:
            cited = _exhibit_numbers(source) | _exhibit_numbers(
                row.cells.get("locator", ""))
            missing = sorted(cited - exhibits)
            if missing:
                findings.append(Finding(
                    "error", row.line, short,
                    "cites exhibit(s) not in the exhibit index: "
                    + ", ".join(str(m) for m in missing)))

    return findings


def check_case(root: pathlib.Path) -> dict:
    """Lint a case folder's registry. Returns a report dict."""
    registry = root / "documents" / "source-registry.md"
    if not registry.exists():
        return {"ok": False, "registry": str(registry), "exists": False,
                "rows": 0, "findings": [], "counts": {},
                "message": "no documents/source-registry.md — build it while "
                           "drafting (references/drafting.md), not after"}

    text = registry.read_text(encoding="utf-8", errors="replace")
    rows, findings = parse(text)

    index = root / "documents" / "exhibit-index.md"
    exhibits = known_exhibits(index.read_text(encoding="utf-8",
                                              errors="replace")) \
        if index.exists() else None

    if not rows:
        findings.append(Finding(
            "error", 0, "",
            "no claim rows found — the registry must hold markdown tables "
            "under '## Load-bearing claims' and '## Supporting facts'"))

    findings += check(rows, exhibits)
    counts = {s: sum(1 for f in findings if f.severity == s)
              for s in ("error", "warn", "decide")}
    return {
        "ok": counts["error"] == 0,
        "registry": str(registry),
        "exists": True,
        "rows": len(rows),
        "load_bearing": sum(1 for r in rows if r.tier == LOAD_BEARING),
        "exhibit_index": bool(exhibits),
        "counts": counts,
        "findings": [f.as_dict() for f in findings],
    }
