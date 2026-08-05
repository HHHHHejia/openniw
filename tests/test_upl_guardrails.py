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


# --------------------------------------------------------------------------
# The reference workflows, not just the top-level rules.
#
# The failure mode this catches is specific and was found in a real audit:
# every SKILL.md carried the right prohibitions while the reference files
# they load still told the agent to pick a tier, recommend filing now, and
# freeze a decision on the user's behalf. A rule that a later file overrides
# is not a rule, so the scan runs over references/ as well.

CONCLUSORY = [
    # verdicts about the person
    r"you qualify", r"you do not qualify", r"you meet (?:this|the) \w+",
    r"criteri(?:on|a) (?:is|are) satisfied", r"prong \d is (?:met|satisfied)",
    r"evidence is (?:legally )?sufficient", r"legally sufficient",
    # decisions belonging to the user
    r"\bfile now\b", r"should (?:not )?file", r"wait before filing",
    r"default recommendation", r"strengthen[- ]first is",
    r"best legal strategy", r"recommended structure", r"best structure",
    r"agent-selected", r"freeze the petitioner structure",
    # outcome talk
    r"approval probabilit", r"guarantee\w* approval", r"will (?:likely )?be approved",
    r"cures? the rfe", r"winning (?:argument|rebuttal)",
    r"officer is (?:legally )?wrong",
    # authority the software does not have
    r"attorney[- ]level", r"lawyer[- ]approved", r"attorney[- ]reviewed",
]

# A phrase inside a prohibition is the rule working, not a violation.
NEGATED = re.compile(
    r"never|not\b|no\b|avoid|decline|refus|forbid|do not|don't|must not|"
    r"cannot|rather than|instead of|stop|prohibit|beyond what",
    re.I)


def _reference_files():
    for skill in ALL_SKILLS:
        yield from sorted((SKILLS / skill / "references").rglob("*.md"))


def test_reference_workflows_do_not_override_the_top_level_rules():
    """Scan every reference file for conclusory instructions. A hit is
    allowed only where the surrounding sentence forbids it."""
    offenders = []
    for path in _reference_files():
        text = path.read_text(encoding="utf-8")
        for pattern in CONCLUSORY:
            for m in re.finditer(pattern, text, re.I):
                line = text[:m.start()].count("\n") + 1
                # wrap-safe window: the negation often sits a line away
                window = text[max(0, m.start() - 200):m.end() + 120]
                if NEGATED.search(window):
                    continue
                rel = path.relative_to(REPO)
                offenders.append(f"{rel}:{line}: {m.group(0)!r}")
    assert not offenders, (
        "conclusory instruction in a reference workflow — it would override "
        "the SKILL.md rule:\n  " + "\n  ".join(offenders))


def test_evaluations_offer_considerations_not_a_filing_verdict():
    """The filing decision is the user's. Each evaluation must say so."""
    for skill in PETITION_SKILLS:
        text = _flat((SKILLS / skill / "references" / "evaluation.md")
                     .read_text(encoding="utf-8"))
        assert "filing-readiness considerations" in text, \
            f"{skill}: evaluation has no filing-readiness section"
        assert "does not decide whether" in text, \
            f"{skill}: evaluation never disclaims the filing decision"
        assert "record-development" in text, \
            f"{skill}: still labels the applicant rather than the record"


def test_the_frame_is_recorded_only_once_the_user_confirms():
    """Endeavor sentence, claim frame and petitioner structure are the
    user's choices; the agent drafts options and records a confirmation."""
    for skill, fname, needle in (
        ("niw-petition", "endeavor.md", "user-confirmed canonical"),
        ("eb1a-petition", "claim-frame.md", "user-confirmed claim frame"),
        ("o1-petition", "petition-frame.md", "user-and-petitioner-confirmed"),
    ):
        text = _flat((SKILLS / skill / "references" / fname)
                     .read_text(encoding="utf-8"))
        assert needle in text, f"{skill}/{fname} does not record a user confirmation"


def test_generated_documents_carry_a_self_help_draft_header():
    for skill in PETITION_SKILLS:
        text = _flat((SKILLS / skill / "references" / "drafting.md")
                     .read_text(encoding="utf-8"))
        assert "self-help draft — not attorney-reviewed" in text, \
            f"{skill}: drafts ship without the self-help header"


def test_maintainer_policy_covers_every_channel():
    text = _flat(POLICY.read_text(encoding="utf-8"))
    for channel in ("github", "email", "social media", "direct message",
                    "donation", "sponsorship"):
        assert channel in text, f"MAINTAINER-POLICY does not name {channel}"
