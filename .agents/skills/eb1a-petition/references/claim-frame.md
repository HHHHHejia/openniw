# Stage II·a — The Claim Frame (compose once, freeze forever)

An EB-1A petition stands on three framing decisions made BEFORE any
drafting. They are recorded in `claim-frame.md`, confirmed by the user,
and then FROZEN: every later document quotes the field definition
verbatim, argues exactly the chosen criteria, and stays inside the intent
scope. Inconsistent field labels or criteria lists across documents are a
classic RFE trigger, and reframing after filing reads as concession.

## 1. The field-of-endeavor definition (the denominator)

"One of that small percentage who have risen to the very top of the
**field of endeavor**" (8 CFR 204.5(h)(2)) — the field definition sets the
comparison pool for everything downstream.
- **Too narrow** ("adversarial robustness of vision transformers under
  distribution shift") looks gamed: the officer sees a field engineered so
  the applicant is its only member, and letters/rankings for such a field
  don't exist.
- **Too broad** ("computer science") raises the bar to the true giants of
  the discipline and makes "small percentage at the very top" unwinnable.
- Right-sized: a recognized subfield with its own venues, societies, and
  rankable metrics ("medical image analysis", "battery materials
  chemistry") in which the applicant's percentile arguments actually work.
- Draft 2-3 candidate definitions, test each against the evidence ("do the
  citation percentiles, venue ranks, and letter writers exist FOR THIS
  FIELD?"), and pick with the user. Write the winner as one quotable noun
  phrase; it goes into case.json and appears VERBATIM in the petition
  letter, the statement, every support letter, and the I-140 worksheet.
- The frozen field must also match the work the person will actually do in
  the U.S. — credentials in field A + intended work in field B is a
  documented denial pattern.

## 2. The 3-5 target criteria (evidence-hierarchy reasoning)

From the Stage I ten-criteria table, choose the criteria the petition will
ARGUE. Rules:
- **Minimum 3 provable; 4 when a 4th is genuinely strong; never pad.** A
  weak claimed criterion gives the officer a place to start writing the
  denial. Real approved research petitions typically file exactly 4.
- The researcher default quad: **(iv) judging + (v) original
  contributions + (vi) scholarly articles**, plus one of (i) awards /
  (viii) critical role / (ix) high salary / (ii) membership.
- For each chosen criterion, decompose into its sub-elements (evidence.md
  lists them) and confirm every sub-element has evidence — missing one
  sub-element is the standard RFE.
- Evidence-hierarchy check: each chosen criterion needs at least one
  Tier-1/Tier-2 anchor (independent third-party record or solicited
  expert/organization letter). A criterion whose best evidence is
  self-generated or colleague-attested is RFE-vulnerable — demote it to
  "reserve" rather than claiming it thin.
- Comparable evidence ((h)(4)) is available when a criterion does not
  readily apply to the occupation (industry researcher: major trade-show
  presentation ≈ scholarly articles; entrepreneur: highly valued startup
  equity ≈ high salary) — it needs a detailed, specific statement of WHY
  the listed criterion doesn't readily apply, so decide it here, not
  mid-draft.

## 3. Intent scope and the prospective-benefit hook

Freeze the scope of the intent-to-continue-work statement
(8 CFR 204.5(h)(5) — for a self-petitioner, a signed first-person
statement of plans is the standard vehicle):
- **Work plan scope**: the concrete line of work in the frozen field the
  person will continue in the U.S. — broad enough to survive a change of
  employer, specific enough to be evidenced (ongoing projects,
  collaborations, a named position or realistic pipeline).
- **Prospective-benefit hook** (INA 203(b)(1)(A)(iii)): one clear
  mechanism by which the continued work benefits the U.S. — the standard
  is interpreted broadly, so a truthful, concrete mechanism (research
  output, clinical/industrial adoption, training capacity) beats grand
  claims. Note it in one sentence here; drafting.md expands it.

## Record in claim-frame.md

```markdown
# Claim Frame (FROZEN 2026-08-02 — do not reword)
## Field of endeavor (verbatim everywhere)
"..."
## Criteria argued
1. (v) original contributions — anchors: [exhibits]; sub-elements: ✓✓
2. (vi) scholarly articles — ...
3. (iv) judging — ...
4. (viii) critical role — ... (or: reserve — reason)
## Intent to continue work — scope
One paragraph: what work continues, where/how, employer-independent.
## Prospective U.S. benefit — hook
One sentence.
```

Once the user confirms, mark it FROZEN with the date. During drafting
review, grep every document for the field phrase and the criteria list —
any drift is a lint failure.

Sources: 8 CFR 204.5(h)(2)-(h)(5); USCIS Policy Manual Vol. 6 Part F
Ch. 2; criterion-selection and evidence-tier patterns adapted from
juntoku9/claude_immigration_attorney (MIT); "file 4 criteria" practice
observed in public approved self-petitions (razvanmarinescu/EB1A,
Ryan-Rhys/EB1A — structure only).
