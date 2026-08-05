"""The i485-adjustment skill is deliberately an assembly tool, not an
eligibility-judgment tool: an I-485 denial for someone without other status
can end in removal proceedings, so the refusals are the product. These tests
pin the properties that make that true, plus the two facts most likely to
rot into a user-harming error.
"""
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[1]
SKILL = REPO / ".agents" / "skills" / "i485-adjustment"
SKILL_MD = SKILL / "SKILL.md"


def _all_text() -> dict[pathlib.Path, str]:
    return {p: p.read_text(encoding="utf-8")
            for p in sorted(SKILL.rglob("*.md"))}


def test_skill_exists_with_expected_references():
    assert SKILL_MD.exists()
    refs = {p.name for p in (SKILL / "references").glob("*.md")}
    assert refs == {"eligibility.md", "history.md", "documents.md",
                    "forms.md", "package.md", "after-filing.md"}, refs


def test_frontmatter_follows_the_house_convention():
    head = SKILL_MD.read_text(encoding="utf-8").split("---")[1]
    assert re.search(r"^name:\s*i485-adjustment\s*$", head, re.M)
    assert "license: MIT" in head
    assert "github.com/HHHHHejia/openniw" in head
    desc = re.search(r"^description:\s*(.+)$", head, re.M)
    assert desc, "no description"
    assert desc.group(1).rstrip().endswith(
        "Document preparation only, not legal advice.")


def test_inadmissibility_block_is_part_9_not_part_8():
    """Edition 01/20/25 renumbered it: Part 8 is Biographic Information and
    Part 9 holds the 86 inadmissibility items. Pointing a user at Part 8
    sends them to the wrong questions."""
    for path, text in _all_text().items():
        for m in re.finditer(r"Part 8\b", text):
            # look on both sides: the qualifier may precede the mention
            # ("edition 07/15/22 numbered it Part 8")
            window = text[max(0, m.start() - 120):m.end() + 90].lower()
            assert ("biographic" in window or "07/15/22" in window
                    or "renumber" in window or "edition" in window), \
                f"{path.name}: 'Part 8' used without the biographic/old-edition " \
                f"qualifier — {text[m.start() - 60:m.end() + 60]!r}"
    assert "Part 9" in SKILL_MD.read_text(encoding="utf-8")


def test_hard_stops_live_in_skill_md_not_only_a_reference():
    """References load when a stage is reached; SKILL.md is always in
    context, and a user can disclose an arrest in their first sentence."""
    # hyphenation varies ("public-charge" / "public charge"), so normalise
    text = SKILL_MD.read_text(encoding="utf-8").lower().replace("-", " ")
    required = [
        "part 9", "criminal", "overstay", "unauthorized", "245(k)",
        "misrepresentation", "removal", "212(e)", "public charge",
        "cspa", "204(j)", "family based",
    ]
    missing = [k for k in required if k.replace("-", " ") not in text]
    assert not missing, f"hard-stop list in SKILL.md is missing: {missing}"


def test_the_skill_never_speaks_in_advice():
    """The whole justification for shipping this is that it does not opine."""
    banned = re.compile(
        r"we recommend|you should file|it is safe to|you are eligible|"
        r"likely to be approved|your chances|we advise", re.I)
    for path, text in _all_text().items():
        for m in banned.finditer(text):
            line = text[:m.start()].count("\n") + 1
            context = text.splitlines()[line - 1]
            # a negated mention ("never recommend", "do not advise") is fine
            assert re.search(r"never|not|refus|decline|forbid", context, re.I), \
                f"{path.name}:{line} reads as advice: {context.strip()!r}"


def test_no_copyrighted_source_material_leaked():
    """The research drew on a law firm's DIY packet marked 'Copyright
    Protected. All Rights Reserved.' Only the process may be reused."""
    fingerprints = [
        "a law firm", "the firm",
        "redacted", "2501 s. state highway", "888.666.0969",
        "elizabeth doe", "charles doe",
        "respectfully submitting this letter in support",
    ]
    for path, text in _all_text().items():
        low = text.lower()
        hits = [f for f in fingerprints if f in low]
        assert not hits, f"{path.name} contains source-packet material: {hits}"


def test_stage_checklist_matches_the_stepper_contract():
    """The browser stepper parses these lines; a drifted format renders no
    progress at all."""
    text = SKILL_MD.read_text(encoding="utf-8")
    rx = re.compile(r"^\s*-\s*\[( |x|X)\]\s+(I{1,3}V?|IV|V)(·[ab])?\s", re.M)
    ids = {m.group(2) + (m.group(3) or "") for m in rx.finditer(text)}
    assert {"I", "II·a", "II·b", "III", "IV", "V"} <= ids, ids


def test_niw_only_companion_commands_are_declined_not_invoked():
    forbidden = ["openniw fill", "openniw ui forms", "openniw package",
                 "openniw harvest", "openniw papers", "openniw fetch-forms",
                 "openniw ui benchmark", "openniw ui citations"]
    for path, text in _all_text().items():
        for cmd in forbidden:
            for m in re.finditer(re.escape(cmd), text):
                line_no = text[:m.start()].count("\n") + 1
                # window, not line: the negation often wraps to the next line
                window = text[max(0, m.start() - 160):m.end() + 160]
                assert re.search(
                    r"\bnot?\b|don't|never|declin|hardwired|irrelevant|"
                    r"instead", window, re.I), \
                    f"{path.name}:{line_no} appears to invoke {cmd}: " \
                    f"{window.strip()!r}"


def test_self_contained_for_npx_install():
    for path, text in _all_text().items():
        assert "/Users/" not in text, f"{path.name} has an absolute path"
        assert "reference/i485" not in text, \
            f"{path.name} points at the research folder, which does not ship"
