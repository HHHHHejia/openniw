# Stage I — Free Evaluation

Produce an honest, prong-by-prong read of the applicant's NIW case from their
public record. Write the result to `evaluation.md` in the case folder.

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
files dropped into `niw-case/sources/` (create the folder first, tell them
the exact path). Wrong place? Copy, don't scold — a path elsewhere
(`~/Downloads/cv.pdf`) or a wrong subfolder gets copied into `sources/`
yourself (standing rule 4), confirmed in one clause.

## Then the benchmark page

After profile.md exists, pre-fill `benchmark.json` with the profile's
citations/papers/field and launch `openniw ui benchmark`. It plots 7,400+
publicly posted approved cases (I-140 categories plus a small O-1 pool):
monthly distribution bands of
approved peers with the user's numbers as reference lines. The page's copy
is survivor-bias-safe (percentile among APPROVED cases, never an approval
probability) — keep your own language consistent with that. After the
session, use `benchmark.json`'s `computed` block (percentiles, peer
medians, low-citation precedents) as hard numbers in the Calibration
section of evaluation.md. No browser? Calibrate from the guidance below.

**Archive everything you fetch.** Every page you download becomes part of
the case record: save it under `sources/fetched/` as
`<YYYY-MM-DD>-<slug>.md` (rendered text; keep raw HTML only if the
rendering loses data) before extracting from it. Two reasons: facts in
profile.md must stay traceable to a dated source, and printed page
captures are themselves exhibit material later. Note the archive path
next to the corresponding entry in the File inventory of STATE.md.

Consolidate into `profile.md`: name, education, positions, field/subfields,
publications (title, venue, venue type, year, authorship position, citations),
metrics, peer-review service, awards, funding, open source, patents, media —
each section noting which `sources/` file it came from.
Mark authorship position only from explicit signals (name order,
equal-contribution notes); never guess.

## Auto-download the applicant's papers (default step, not optional)

As soon as the publication list exists in profile.md, batch-download the
papers WITHOUT being asked — they are needed as exhibits (Stage II·b) and
for your own reading:

    openniw papers "Title 1" "Title 2" ...
    (fallback: python3 scripts/fetch_papers.py "Title 1" ...)

This resolves each title on OpenAlex and pulls the best open-access PDF
(arXiv, PubMed Central, publisher OA) into `sources/papers/` with a
provenance manifest. Then report the outcome and hand the gaps to the user
in one message:
- **downloaded** — say how many, done.
- **preprint_only** — the published version is the preferred exhibit: list
  these and ask the user to download the published PDFs via their
  institutional access into `sources/papers/` (suggest the exact filename
  from the manifest).
- **no_oa_pdf / unresolved / failed** — list each title and ask the user
  to drop the PDF into `sources/papers/` manually (or give you a path —
  you copy it in, standing rule 4).

Track the missing ones as an open item in STATE.md until every paper in
profile.md has a PDF in `sources/papers/`.

## Legal framework to apply

1. EB-2 threshold: advanced degree (or bachelor's + 5 years progressive
   experience) or exceptional ability.
2. Matter of Dhanasar, 26 I&N Dec. 884 (AAO 2016):
   - Prong 1: the proposed endeavor has substantial merit AND national importance
   - Prong 2: the person is well positioned to advance it (education, record,
     plan, progress, interest of relevant parties)
   - Prong 3: on balance, waiving the job-offer/labor-cert requirement benefits
     the U.S.
3. USCIS Policy Manual update (Jan 15, 2025) — stricter scrutiny:
   - The degree must relate DIRECTLY to the proposed endeavor
   - The occupation underlying the endeavor must itself be a profession
     (bachelor's-required) — full gate in endeavor.md; apply it here too
   - Broad "benefits the economy" claims are insufficient; tie to specific
     national priorities (CET areas, agency frameworks, federal targets)
   - Entrepreneur claims need concrete support: funding, contracts, letters of
     interest, active central role in a U.S. entity
   - Letters alone are insufficient — they must be "supported by other
     independent evidence"; unsubstantiated claims fail the burden of proof

## Calibration (what strong filings actually look like)

Strong signals: citation count and per-year percentile, h-index, first-authored
papers in ranked venues, peer-review count, federal/major funding, competitive
awards with selectivity ratios, open-source adoption metrics, independent
researchers building on the work. A specific well-scoped endeavor matters as
much as credentials. RFE triggers to warn about: vague endeavor ("continue my
research"), degree–endeavor mismatch, no evidence of third-party use,
everything tied to one employer.

## Adjudication climate (as of 2026-08-02 — refresh quarterly)

USCIS publishes no official NIW approval/RFE-rate page; every figure below
is a practitioner tally of USCIS quarterly I-140 data, and counting methods
differ across trackers — so always state period + source together, never a
bare number.
- Approval rate: ~95.7% FY2022 (visafranchise/manifestlaw, USCIS data) →
  ~43.3% FY2024 (calivisa) → ~42.6% Q1 FY2026, Oct–Dec 2025 (visafranchise).
  Drivers: ~3× filing volume since FY2022 + the Jan-2025 policy tightening.
- RFE rate, regular processing: ~50% Jan 2026 → ~39% Mar 2026 (Lawfully
  tracking via manifestlaw).
- AAO appeals are near-futile: FY2021–FY2025, 64 sustained vs 2,831
  dismissed, ~2.2% (published tally) — the initial filing must be right.
- Premium processing accelerates outcomes, not odds.
What this climate means for the write-up: it raises the value of naming gaps
plainly and early. It does not license a verdict. These are population rates
among adjudicated petitions — never present any of them as this applicant's
approval probability, and never convert them into advice about whether or when
to file.

## Output format (evaluation.md)

1. **Summary** — 2-3 sentences, direct.
2. **Record-development level** — one of `well-developed` / `developing` /
   `substantial gaps` / `insufficient information`, one-line reason. Print
   beneath it, verbatim: *"This is a software-generated record-development
   indicator, not a legal eligibility determination or approval prediction."*
   It describes how far the RECORD has been built, never whether the applicant
   qualifies.
3. **Prong-by-prong analysis** — for each prong, four headed lists:
   - *Potentially supportive facts* — cite the profile's actual numbers
   - *Potential weaknesses or limiting facts*
   - *Unresolved questions* — what is not yet knowable from the record
   - *Possible evidence categories for the user's consideration*
   - *Drafting implications* — what this means for how the argument is built

   Score each prong 1-5 if it helps you organise the work; the score is a
   record-maturity marker for drafting, not a finding that a prong is met.
   Never write that a prong is satisfied, met, or established.
4. **Suggested endeavor angles** — 2-3 concrete framings tied to named U.S.
   priorities for their field, presented as options for the user to weigh.
5. **Evidence to gather** — prioritized.
6. **Filing-readiness considerations** — replaces any verdict. Use this shape:

   > The current record appears to contain the following developed components:
   > …
   > The following components remain incomplete, weakly documented, or
   > dependent on unresolved facts: …
   > Submitting with the current record may involve the following risks: …
   > Further record development could include: …
   >
   > OpenNIW does not decide whether or when you should file. That decision is
   > yours, and is worth taking to a licensed immigration attorney first.

   Be concrete about gaps and risks — vagueness here is its own disservice.
   What changes is only that the conclusion stays with the user.

Never invent facts. End with: "This is software-generated self-help analysis
for your independent review, not legal advice and not an eligibility
determination."

Sources: USCIS Policy Manual Vol. 6 Pt. F Ch. 5 (incl. Jan 15, 2025 update)
· visafranchise.com/blog/eb2-niw-approval-rate · manifestlaw.com/blog/
eb2-niw-approval-rate · calivisa.com (FY2024 stats post) · a published 2026
adjudication-shifts post and AAO tally. Rates checked 2026-08-02.
