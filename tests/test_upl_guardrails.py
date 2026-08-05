"""Guardrails that keep the project on the safe side of the line between
publishing self-help software and practising law.

Reviewed by outside counsel-style analysis in 2026-08: the risk lives in
what the skills instruct an agent to *conclude*, in how the site advertises
what the software does, and in whether the maintainers ever touch an
individual case. These tests pin all three so a later edit cannot quietly
undo them.
"""
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[1]
SKILLS = REPO / ".agents" / "skills"
ALL_SKILLS = ("niw-petition", "eb1a-petition", "o1-petition",
              "i485-adjustment")
PETITION_SKILLS = ("niw-petition", "eb1a-petition", "o1-petition")
SITE = REPO / "webpage" / "app" / "page.tsx"
FOOTER = REPO / "webpage" / "components" / "nav.tsx"
POLICY = REPO / "MAINTAINER-POLICY.md"


def _skill_md(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """Collapse whitespace: these files wrap at ~76 columns, so any phrase
    can be split across a newline mid-check."""
    return re.sub(r"\s+", " ", text).lower()


def test_maintainer_policy_exists_and_declines_case_help():
    assert POLICY.exists(), "MAINTAINER-POLICY.md is the record that the " \
                            "maintainers never touch an individual case"
    t = POLICY.read_text(encoding="utf-8").lower()
    for phrase in ["do i qualify", "should i file", "rfe",
                   "licensed immigration attorney"]:
        assert phrase in t, f"maintainer policy no longer covers {phrase!r}"
    # paying must not buy case help
    assert re.search(r"pay|donat|sponsor", t), \
        "policy must say that paying or donating changes nothing"


def test_site_and_readme_link_the_maintainer_policy():
    for path in (SITE, REPO / "readme.md"):
        assert "MAINTAINER-POLICY.md" in path.read_text(encoding="utf-8"), \
            f"{path.name} does not point at the maintainer policy"


def test_no_absolute_provide_no_service_claim():
    """'We provide no service' is attackable — software is arguably a
    service. State the precise, defensible facts instead."""
    for path in (SITE, FOOTER, REPO / "readme.md"):
        text = path.read_text(encoding="utf-8")
        assert not re.search(r"provide no service", text, re.I), \
            f"{path.name} makes the absolute 'provide no service' claim"


def test_site_does_not_advertise_legal_judgment():
    """Marketing that promises judgment or predicts what officers want is
    the part a regulator reads first."""
    text = SITE.read_text(encoding="utf-8")
    banned = [
        r"the BRAIN — judgment",
        r"gives an honest read",
        r"shape officers expect",
        r"diagnosis of every challenged point",
    ]
    for pattern in banned:
        assert not re.search(pattern, text, re.I), \
            f"landing page still claims: {pattern}"


def test_site_states_the_software_does_not_decide_eligibility():
    text = SITE.read_text(encoding="utf-8").lower()
    assert "does not decide whether you qualify" in text \
        or "does not determine eligibility" in text, \
        "the landing page must say the software does not decide eligibility"


def test_every_skill_disclaims_case_representation():
    for name in ALL_SKILLS:
        t = _flat(_skill_md(name))
        assert "not legal advice" in t
        assert "no attorney-client relationship" in t
        assert re.search(r"do not work on anyone's case|"
                         r"no case representation", t), \
            f"{name} does not disclaim case representation"


def test_petition_skills_repeat_the_disclaimer_at_checkpoints():
    """Once at session start is not enough — the user meets the risky
    moments hours later."""
    for name in PETITION_SKILLS:
        t = _skill_md(name)
        assert re.search(r"repeat it at (five|four|three) points", _flat(t)), \
            f"{name} does not force a repeat disclaimer at the risky stages"


def test_skills_forbid_stating_the_legal_conclusion():
    for name in PETITION_SKILLS:
        t = _skill_md(name)
        assert "never state the conclusion" in _flat(t), \
            f"{name} lost the no-conclusion rule"
        low = _flat(t)
        for must in ["you qualify", "sufficient", "odds",
                     "re-characterize", "whether, when"]:
            assert must in low, f"{name} no-conclusion rule is missing {must!r}"


def test_skills_refuse_to_phrase_around_adverse_facts():
    for name in ALL_SKILLS:
        t = _flat(_skill_md(name))
        assert re.search(r"conceal|minimi[sz]e|phrase around", t), \
            f"{name} does not refuse to soften adverse facts"


def test_rfe_workflows_hard_stop_on_fraud_and_credibility():
    """An RFE is already a scrutinised record; some notices are the visible
    edge of a fraud referral."""
    needed = ["fraud", "credibility", "material change", "criminal",
              "revocation", "investigation"]
    for name in PETITION_SKILLS:
        t = _flat((SKILLS / name / "references" / "rfe-response.md")
                  .read_text(encoding="utf-8"))
        assert "hard stops" in t, f"{name} rfe-response.md has no hard stops"
        missing = [k for k in needed if k not in t]
        assert not missing, f"{name} RFE hard stops missing: {missing}"
        assert re.search(r"predict the outcome|never.{0,40}overcome", t), \
            f"{name} does not forbid predicting the RFE outcome"
