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
publicly posted approved I-140 cases: monthly distribution bands of
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
   - Broad "benefits the economy" claims are insufficient; tie to specific
     national priorities (CET areas, agency frameworks, federal targets)
   - Entrepreneur claims need concrete support: funding, contracts, letters of
     interest, active central role in a U.S. entity

## Calibration (what strong filings actually look like)

Strong signals: citation count and per-year percentile, h-index, first-authored
papers in ranked venues, peer-review count, federal/major funding, competitive
awards with selectivity ratios, open-source adoption metrics, independent
researchers building on the work. A specific well-scoped endeavor matters as
much as credentials. RFE triggers to warn about: vague endeavor ("continue my
research"), degree–endeavor mismatch, no evidence of third-party use,
everything tied to one employer.

## Output format (evaluation.md)

1. **Summary** — 2-3 sentences, direct.
2. **Tier** — strong / promising / borderline / not-yet, one-line reason.
3. **Prong-by-prong analysis** — strengths (cite the profile's actual numbers),
   gaps, and what evidence would fix each gap. Score each prong 1-5.
4. **Suggested endeavor angles** — 2-3 concrete framings tied to named U.S.
   priorities for their field.
5. **Evidence to gather now** — prioritized.
6. **Bottom line** — file now vs strengthen first, honestly.

Never invent facts. End with: "This is informational analysis, not legal advice."
