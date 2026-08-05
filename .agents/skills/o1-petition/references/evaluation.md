# Stage I — Free Evaluation (O-1A)

Produce an honest, criterion-by-criterion read of the applicant's O-1A case
from their public record. Write the result to `evaluation.md` in the case
folder.

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
files dropped into `o1-case/sources/` (create the folder first, tell them
the exact path). Wrong place? Copy, don't scold — a path elsewhere
(`~/Downloads/cv.pdf`) or a wrong subfolder gets copied into `sources/`
yourself (standing rule 4), confirmed in one clause.

Consolidate into `profile.md`: name, education, positions, field/subfields,
publications (title, venue, venue type, year, authorship position,
citations), metrics, peer-review service, awards, funding, open source,
patents, media, salary history (with the user's consent — it is a
criterion here), company/entity facts if a founder. Mark authorship
position only from explicit signals; never guess.

## Auto-download the applicant's papers (default step, not optional)

As soon as the publication list exists in profile.md, batch-download the
papers WITHOUT being asked — they are needed as exhibits (Stage II·b) and
for your own reading:

    openniw papers "Title 1" "Title 2" ...
    (fallback: python3 scripts/fetch_papers.py "Title 1" ...)

Report the outcome and hand the gaps to the user in one message
(downloaded / preprint_only — ask for the published PDFs / no_oa_pdf,
unresolved, failed — ask for manual drops into `sources/papers/`). Track
the missing ones as an open item in STATE.md.

## Legal framework to apply

1. **The O-1A test** (8 CFR 214.2(o)(3)(iii)): receipt of a major,
   internationally recognized award (Nobel-class), OR at least **3 of 8**
   criteria — in regulatory order: (1) nationally/internationally
   recognized prizes or awards for excellence; (2) membership in
   associations requiring outstanding achievements, judged by recognized
   experts; (3) published material in professional/major media ABOUT the
   beneficiary; (4) judging the work of others (panel or individual);
   (5) original scientific, scholarly, or business-related contributions
   of major significance; (6) authorship of scholarly articles;
   (7) employment in a critical or essential capacity for organizations
   with a distinguished reputation; (8) high salary or other remuneration,
   past OR prospective ("will command"). Comparable evidence is allowed
   when a criterion doesn't readily apply to the occupation.
2. **Two-step adjudication** (Policy Manual Vol. 2 Part M, Ch. 4): first
   the evidentiary count, then a totality determination that the person is
   among "the small percentage who have arisen to the very top of the
   field" with sustained national or international acclaim. Meeting 3
   criteria does not automatically win; plan for the totality stage too
   (high-impact venues, citations/h-index relative to field, leading
   institutions, invited talks, named investigator on U.S. government
   grants, interested-agency letters).
3. **The work, not just the person**: the U.S. work must be in the "area
   of extraordinary ability" — read broadly since 2022 to include related
   occupations sharing the skillset (STEM professor → industry, engineer →
   founder) — and must relate to an event or activity (a job, a scientific
   or business project, an academic year all qualify). The position itself
   need NOT require an extraordinary person.
4. **A petitioner must exist.** Self-petition is prohibited; flag in the
   evaluation which petitioner path (employer / agent / own entity) looks
   viable — the decision itself is Stage II·a.

## Bar comparison and the bridge (put both in every evaluation)

- **vs EB-1A**: the same criteria family (O-1A's 8 track 8 of EB-1A's 10)
  and near-identical "very top of the field" wording, but O-1A is a
  nonimmigrant adjudication and practitioners consistently report its
  totality review applied more flexibly — in practice 3 credible criteria
  usually carry an O-1A, while EB-1A denials concentrate at final merits.
  Practitioner-reported pattern, not an official standard; approval of one
  never compels the other.
- **O-1 as bridge to EB-1A**: O-1 is quasi-dual-intent (8 CFR
  214.2(o)(13): a filed I-140 is no basis for denial). Tell the user what
  to build during O-1 years for the later EB-1A: recurring judging
  (editorial boards, grant panels), media where THEY are the subject,
  competitive awards, measurable adoption of their contributions, salary
  progression, letters from non-collaborators.

## Calibration (percentile among publicly posted APPROVED cases — small sample)

Pre-write `benchmark.json` with `{"category": "O1", field, citations,
publications}` and open `openniw ui benchmark` — the page has an O1 pool
(123 cases) and shows its own small-pool banner. (Older companion builds
have no O1 option in the picker; then calibrate in chat instead.) Either
way, anchor the discussion on these numbers — 123 O-1/O-1A approvals
publicly posted by one research-focused U.S. law firm, 2013–2026
(database snapshot 2026-08):
- citations: P25 111 · **median 261** · P75 491 (2024+ median 208)
- publications: P25 10 · **median 15** · P75 24 (2024+ median 13)
- every case that disclosed a processing mode used premium processing;
  median reported pendency 13 days
- ladder position: this O-1 pool's citation median sits ~2.5× above the
  same database's NIW median (publications ~1.5×), and both sit below
  its recent EB-1A medians.

MANDATORY wording: "your X exceeds ~N% of publicly posted APPROVED O-1
cases in this 123-case sample" — never an approval probability or odds.
Always attach the caveats: tiny sample from one firm's research-heavy
clientele; approved cases only (no denominator); self-reported; says
little about profiles built on entrepreneurial, industry, arts, or
athletic evidence where citations may be irrelevant entirely.

## Output format (evaluation.md)

1. **Summary** — 2-3 sentences, direct.
2. **Record-development level** — one of `well-developed` / `developing` /
   `substantial gaps` / `insufficient information`, one-line reason,
   followed verbatim by: *"This is a software-generated record-development
   indicator, not a legal eligibility determination or approval
   prediction."*
3. **Criterion-by-criterion map** — all 8 (regulatory numbering), each with:
   *Facts potentially supporting it* · *Facts potentially weakening it or
   leaving it unresolved* · *Unresolved issues* · *Evidence-development
   considerations*, citing the profile's actual numbers. Note the
   major-award path only if plausibly real. Never write that a criterion is
   met or satisfied.
4. **Totality read** — which plus-factors the record documents and which it
   does not.
5. **Petitioner-path preview** — what employer / agent / own-entity would
   each require, and which look factually available on what is known so far.
   The choice itself is made by the user and the actual petitioner in
   Stage II·a; do not pre-select one here.
6. **Calibration** — the percentile sentences with caveats, as above.
7. **Evidence to gather** — prioritized.
8. **Filing-readiness considerations** — never a verdict. What the record
   already documents · what remains incomplete or unresolved · risks of
   filing as it stands · what further development could include. If the user
   also asks about green cards, lay out the O-1A → EB-1A/NIW ladder as
   context, not as a recommended sequence. Close with: *"OpenNIW does not
   decide whether or when a petition should be filed. That decision belongs
   to you and your petitioner, and is worth taking to a licensed
   immigration attorney first."*

Never invent facts. End with: "This is software-generated self-help analysis
for your independent review, not legal advice and not an eligibility
determination."

Sources: 8 CFR 214.2(o) (eCFR); USCIS Policy Manual Vol. 2 Part M Ch. 4
(uscis.gov/policy-manual/volume-2-part-m-chapter-4); calibration from an
independent database of public approval notices (2026-08);
practitioner benchmarks: gojumpstart.com, manifestlaw.com.
