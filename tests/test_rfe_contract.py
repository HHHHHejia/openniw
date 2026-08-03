"""The RFE stage (R) is a contract between three artifacts:

- each skill's SKILL.md, which tells the agent what line to append to the
  STATE.md stage checklist,
- frontend/components/session.tsx, whose parseStages regex renders the
  stepper from that checklist,
- .github/ISSUE_TEMPLATE/data-point.yml, whose field ids and dropdown
  options the skills' R7 step must prefill.

Drift in any one of them fails silently in front of a user on a deadline,
so it is checked here.
"""
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[1]
SKILLS = REPO / ".agents" / "skills"
SESSION_TSX = REPO / "frontend" / "components" / "session.tsx"
ISSUE_FORM = REPO / ".github" / "ISSUE_TEMPLATE" / "data-point.yml"

SKILL_NAMES = ("niw-petition", "eb1a-petition", "o1-petition")

# The exact line the skills instruct the agent to append. Mirrors the
# stepper's expectation: checkbox, the bare id "R", then whitespace.
R_LINE = "- [ ] R    RFE"


def _stepper_regex() -> re.Pattern:
    """Lift parseStages' regex out of the TSX so the test breaks when it
    changes rather than quietly diverging from it."""
    src = SESSION_TSX.read_text()
    m = re.search(r"line\.match\(/(.+?)/\)", src)
    assert m, "parseStages regex not found in session.tsx"
    ts = m.group(1)
    return re.compile(ts.replace("\\\\s", "\\s"))


def test_stepper_regex_matches_the_documented_r_line():
    rx = _stepper_regex()
    m = rx.match(R_LINE + "        ← in progress")
    assert m, f"stepper regex {rx.pattern!r} does not match {R_LINE!r}"
    assert m.group(2) == "R"


def test_every_skill_documents_the_exact_r_line():
    for name in SKILL_NAMES:
        text = (SKILLS / name / "SKILL.md").read_text()
        assert R_LINE in text, f"{name}/SKILL.md lost the literal R checklist line"


def test_every_skill_warns_about_the_stale_current_marker():
    """parseStages latches on the FIRST line carrying an arrow, so a stale
    marker above R steals the highlight. Each skill must say so — wording is
    the author's, but the latch rule has to be stated."""
    latch = re.compile(r"first[^.]{0,40}(?:arrow|←)", re.I)
    for name in SKILL_NAMES:
        text = (SKILLS / name / "SKILL.md").read_text()
        assert "←" in text and latch.search(text), \
            f"{name}/SKILL.md does not explain the first-arrow-wins stepper rule"


def test_r7_field_ids_exist_in_the_issue_form():
    """R7 prefills the GitHub issue form by field id; invented ids drop
    silently on submission."""
    form = ISSUE_FORM.read_text()
    ids = set(re.findall(r"^\s*id:\s*([a-z_]+)\s*$", form, re.M))
    expected = {"category", "field", "citations", "publications",
                "filing_month", "premium", "rfe", "outcome",
                "processing_days", "suggestion"}
    assert expected <= ids, f"issue form is missing ids: {expected - ids}"
    for name in SKILL_NAMES:
        rfe_md = (SKILLS / name / "references" / "rfe-response.md").read_text()
        cited = {i for i in expected if i in rfe_md}
        assert len(cited) >= 8, \
            f"{name}/references/rfe-response.md names only {len(cited)} form fields"


def test_skills_do_not_invent_issue_form_fields():
    form_ids = set(re.findall(r"^\s*id:\s*([a-z_]+)\s*$", ISSUE_FORM.read_text(), re.M))
    for name in SKILL_NAMES:
        rfe_md = (SKILLS / name / "references" / "rfe-response.md").read_text()
        # query-string params in a prefill URL are the machine-checkable part
        params = set(re.findall(r"[?&]([a-z_]{4,})=", rfe_md))
        invented = params - form_ids - {"template", "labels", "title", "body"}
        assert not invented, f"{name} prefills unknown issue-form fields: {invented}"
