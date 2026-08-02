# Stage I — Free Evaluation

Produce an honest, prong-by-prong read of the applicant's NIW case from their
public record. Write the result to `evaluation.md` in the case folder.

## Open with the benchmark page (default first move)

Before (or while) gathering sources, launch the visual peer comparison —
`openniw ui benchmark` (Browser sessions rules apply; step owns
`benchmark.json`). It plots 7,400+ publicly posted approved I-140 cases:
the user picks category/field and enters citations/papers, sees the
monthly distribution bands of approved peers with their own number as a
reference line, and clicks "Save to my case". The page's copy is
survivor-bias-safe (percentile among APPROVED cases, never an approval
probability) — keep your own language consistent with that.

After the session, read `benchmark.json` and use its `computed` block
(percentile, peer medians, low-citation precedents) as hard numbers in the
Calibration section of evaluation.md. No browser/companion? Skip the page;
calibrate from the guidance below instead.

## Gather sources first

Ask only for links/files, never for typed-out lists — and be explicit about
HOW to hand each one over:
- **Links — paste right here in the chat**: Google Scholar profile URL
  (fetch it: name, affiliation, citations, h-index, per-paper cited-by
  counts, publication list), personal homepage URL, lab/company pages.
- **Files — tell the user exactly where to put them**: "drop your CV (and
  any other documents) into `niw-case/sources/` and tell me when done" —
  create the folder first so it exists when they look for it. LinkedIn
  blocks robots: ask for its "Save to PDF" export into `sources/`, or
  pasted text.
- **Wrong place? Copy, don't scold.** If they give a path elsewhere
  (`~/Downloads/cv.pdf`), name a file in another folder, or drop it in the
  wrong subfolder — copy it into `sources/` yourself (standing rule 4),
  confirm in one clause ("copied to sources/cv.pdf"), and move on.

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
