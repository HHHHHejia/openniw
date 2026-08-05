# Stage I — Free Evaluation

Produce an honest, criterion-by-criterion read of the applicant's EB-1A
case from their public record. Write the result to `evaluation.md` in the
case folder.

## Open with the intake page (default first move)

Launch `openniw ui intake` as the very first act of a new case (Browser
sessions rules; step owns `intake.json` + `sources/`). In the browser the
user: pastes links (Scholar / homepage / LinkedIn / other), drags files
(CV, LinkedIn "Save to PDF" export) straight into `sources/`, and answers
the fixed basics (position, degree, field, in-U.S.). Tell them what
happens next: "when you click Done there, come back here — I'll fetch and
analyze everything." On Done, read `intake.json` and the `sources/`
listing, then do the non-standard half yourself:
- fetch every link, archiving each page under `sources/fetched/` as
  `<YYYY-MM-DD>-<slug>.md` before extracting (facts must stay traceable;
  page captures are exhibit material later);
- read every uploaded file;
- consolidate into profile.md, each section noting its source file.

**Chat fallback** (no browser/companion): ask for links pasted in chat and
files dropped into `eb1a-case/sources/` (create the folder first, tell them
the exact path). Wrong place? Copy, don't scold — a path elsewhere
(`~/Downloads/cv.pdf`) or a wrong subfolder gets copied into `sources/`
yourself (standing rule 4), confirmed in one clause.

Consolidate into `profile.md`: name, education, positions, field/subfields,
publications (title, venue, venue type, year, authorship position,
citations), metrics, peer-review service, awards, memberships, funding,
open source, patents, media, salary if volunteered — each section noting
which `sources/` file it came from. Mark authorship position only from
explicit signals (name order, equal-contribution notes); never guess.

## Auto-download the applicant's papers (default step, not optional)

As soon as the publication list exists in profile.md, batch-download the
papers WITHOUT being asked — they are needed as exhibits (Stage II·b) and
for your own reading:

    openniw papers "Title 1" "Title 2" ...
    (fallback: python3 scripts/fetch_papers.py "Title 1" ...)

This resolves each title on OpenAlex and pulls the best open-access PDF
into `sources/papers/` with a provenance manifest. Report the outcome in
one message: **downloaded** (count); **preprint_only** (ask for the
published PDFs via institutional access — the preferred exhibit);
**no_oa_pdf / unresolved / failed** (ask the user to drop each PDF in, or
give you a path to copy). Track gaps in STATE.md until every paper has a
PDF.

## Then the benchmark page

After profile.md exists, pre-write `benchmark.json` in the case folder:

```json
{"category": "EB1A", "field": "<closest dropdown field>",
 "citations": <total>, "publications": <count>}
```

then launch `openniw ui benchmark`. The page reads the saved category and
plots the user's numbers against ~2,300 publicly posted approved EB-1A
cases (part of a 7,400+ approved-case pool). Its copy is
survivor-bias-safe — "percentile among publicly posted APPROVED cases",
never an approval probability — keep your own language identical. Use the
`computed` block it saves (percentiles, peer medians, low-citation
precedents) as hard numbers in evaluation.md's Calibration section. No
browser? Calibrate from the guidance below.

## Legal framework to apply

1. Statute — INA 203(b)(1)(A), three required showings: (i) extraordinary
   ability demonstrated by **sustained national or international acclaim**
   with achievements recognized through extensive documentation; (ii) the
   person seeks to enter the U.S. to **continue work in the area** of
   extraordinary ability; (iii) entry will **substantially benefit
   prospectively** the United States (interpreted broadly — *Matter of
   Price*, 20 I&N Dec. 953).
2. Regulation — 8 CFR 204.5(h): extraordinary ability = "one of that small
   percentage who have risen to the very top of the field of endeavor"
   ((h)(2)); self-petition allowed ((h)(1)); no job offer or labor
   certification, but the petition must show intent to continue work —
   a beneficiary statement of plans suffices ((h)(5)). Initial evidence =
   a one-time major internationally recognized award (Nobel-class) OR at
   least **3 of the 10 criteria** ((h)(3)(i)-(x)): (i) prizes/awards ·
   (ii) exclusive memberships · (iii) published material about the
   person · (iv) judging · (v) original contributions of major
   significance · (vi) scholarly articles · (vii) artistic exhibitions ·
   (viii) leading/critical role · (ix) high salary · (x) performing-arts
   commercial success (full bars and traps per criterion: evidence.md).
   Comparable evidence allowed when a criterion does not readily apply to
   the occupation ((h)(4)).
3. *Kazarian v. USCIS*, 596 F.3d 1115 (9th Cir. 2010) — the two-step test
   the officer applies and your evaluation must mirror:
   - **Step 1**: does the evidence objectively meet ≥3 criteria
     (preponderance standard, no top-of-field judgment yet)?
   - **Step 2 — final merits**: does the totality show sustained acclaim
     and top-small-percentage standing? This is where most petitions die.
4. Policy Manual Vol. 6 Part F Ch. 2 (as of mid-2026) — apply the Oct 2,
   2024 clarifications: team awards count if the person is a named
   recipient; past memberships count; published material need NOT
   demonstrate the value of the work; exhibitions must be artistic
   (non-artistic only via comparable evidence). Re-check the live chapter
   before filing — this manual moves.

## Calibration (what publicly posted approved EB-1A cases look like)

Among ~2,300 publicly posted approved EB-1A cases (heavily STEM-PhD; one
firm's published wins, so likely inflated vs the true approved pool), the
2024+ era medians are ≈590 citations and ≈19 publications overall — by
field: CS/AI ≈713 · engineering/materials ≈499 · life sciences ≈575 ·
medicine ≈575 · physics/math ≈757 citations. Approved EB-1A profiles run
roughly 3-5.5× the citations and ~2× the publications of approved NIW
profiles in the same field. Low-citation approvals exist but share one
shape: a *rankable* distinction (top-cited paper in a venue, a real prize,
an adopted artifact) substituting for volume. Always present these as
"percentile among publicly posted APPROVED cases", never as approval odds;
flag any per-field slice under ~30 cases as unstable. Field-normalized
percentile beats raw count; per-paper impact beats aggregates.

## Visa-bulletin reality check (as of 2026-08 — verify the current bulletin)

EB-1 is current for most countries, but **China and India are badly
retrogressed** (Aug 2026 final action dates ≈ Jul 2023 / Oct 2022; dates
verified only via secondary summaries — re-check travel.state.gov).
Retrogression does NOT change whether or when to file the I-140: filing
locks the **priority date** (the day USCIS receives the complete, signed
I-140 with correct fee), and that date is the asset. It DOES change the
back end: China/India-chargeable petitioners generally cannot file I-485
concurrently; ROW petitioners can, though practitioners often prefer
sequential-with-premium so the I-485 never rides on an undecided I-140.

## Output format (evaluation.md)

1. **Summary** — 2-3 sentences, direct.
2. **Ten-criteria map** — every criterion (i)-(x) with, under each:
   *Facts potentially supporting this criterion* · *Facts potentially
   weakening it or leaving it unresolved* · *Unresolved issues* ·
   *Evidence-development considerations*. Cite the profile's actual numbers
   and name the strongest exhibit that would document each point. Never
   write that a criterion is met, satisfied, or established — that is the
   adjudicator's finding, not yours.
3. **Two-step structure (Kazarian)** — Step 1: which criteria the record
   currently documents most fully, and which rest on facts still to be
   obtained. Step 2: how developed the final-merits narrative is
   (multi-year arc, independent adoption, field-elite comparison). Say
   plainly where either is thin — that is useful; a verdict on either is
   not yours to give.
4. **Record-development level** — one of `well-developed` / `developing` /
   `substantial gaps` / `insufficient information`, one-line reason,
   followed verbatim by: *"This is a software-generated record-development
   indicator, not a legal eligibility determination or approval
   prediction."*
5. **Calibration** — benchmark percentiles with the approved-cases wording.
6. **Evidence-development plan** — prioritized, per thinly documented
   criterion.
7. **Filing-readiness considerations** — never a verdict. What the record
   already documents · what remains incomplete or unresolved · risks of
   submitting as it stands · what further development could include. Where
   the record is thinner for EB-1A than for NIW, lay out the routes without
   choosing between them: NIW-first then EB-1A later (an approved NIW
   priority date ports under 8 CFR 204.5(e)); concurrent NIW+EB-1A (two
   I-140s, two fees, and a known risk of narrative inconsistency between
   the filings). Close with: *"OpenNIW does not decide whether, when, or in
   which category you should file. That choice is yours, and is worth
   taking to a licensed immigration attorney first."*

Never invent facts. End with: "This is software-generated self-help analysis
for your independent review, not legal advice and not an eligibility
determination."

Sources: 8 CFR 204.5(h) (ecfr.gov); INA 203(b)(1)(A); USCIS Policy Manual
Vol. 6 Part F Ch. 2 (uscis.gov/policy-manual/volume-6-part-f-chapter-2);
Kazarian v. USCIS, 596 F.3d 1115 (9th Cir. 2010); Aug 2026 visa bulletin
via Fragomen/Ogletree summaries (primary blocked); calibration from a local
snapshot of public approval notices (2026-08).
