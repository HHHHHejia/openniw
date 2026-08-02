# Stage II·b — Evidence Collection & The Citation Pipeline

Maintain `evidence/checklist.md` as a ledger: one line per item with status
(`suggested | needed | provided | na`), and `evidence/exhibits/` for files.
Objective evidence beats subjective: every claim a letter makes must be
shadowed by an objective exhibit. Build the exhibit index FROM the claims.

## Checklist taxonomy (personalize; drop irrelevant, add case-specific)

identity/status · degrees (diploma + official transcript + NACES general
evaluation for foreign degrees; current PhD students add an enrollment/
candidacy verification letter) · CV · publications · conference
presentations · venue rankings & selectivity · citation record ·
peer-review service · awards · funding · open source · patents · media ·
certified translations · endeavor-support evidence · employment letter ·
recommenders (+ each recommender's CV, max 5 pages, or a bio page).

Per-type evidence specs (from real successful filings):
- **Publications**: official published version, first 3-5 pages per exhibit,
  applicant's name highlighted, venue+year visible. Accepted-but-unpublished:
  attach acceptance email/forum page. Books: cover + TOC + © page + 3 pages.
- **Conference presentations** (oral/poster): program or schedule first page
  + the page listing the talk, name highlighted; poster PDF or session
  photos also work.
- **Venue rankings & selectivity**: Google Scholar Metrics or CORE ranking
  page per venue, journal impact factors, published acceptance rates
  ("Acceptance Rate: 22%").
- **Translations**: EVERY foreign-language document needs a full English
  translation + the translator's signed certification (complete, accurate,
  competent to translate).
- **Citation record**: Google Scholar ONLY (multiple databases confuse
  officers and invite RFEs). Print the profile to PDF, logged out.
- **Peer review**: per-review email trails (invitation → acceptance/assignment
  → completion). Publons alone is no longer accepted. Reviews of revised
  manuscripts count separately only with proof of two rounds.
- **Awards**: notice + public page + selection criteria (N selected out of M).
  No student awards.
- **Funding**: award pages naming the person, or paper acknowledgments.
  Phrase as "participated in projects funded by X" — never "grantee".
- **Open source**: repo page + PR/issues pages, logged out, URL visible, dated.
- **Media**: applicant must be NAMED; employer/university press releases
  excluded. Foreign-language items need certified translation + original.
- **Screenshots**: full URL visible, captured logged-out.
- Date-class every exhibit: pre-filing / post-filing. Eligibility is judged
  AS OF the filing date; post-filing evidence only works as continuation.

## The citation pipeline (the highest-value automation)

Run `scripts/harvest_citations.py "Title 1" "Title 2" ...` — it pulls every
citing paper from OpenAlex with authors/venue/OA-PDF links and screens:
independence (exact-name match ⇒ dependent; family+initial collision ⇒
conservatively dependent + flagged; family-only ⇒ independent + flagged) and
published-only (no preprints/posters/under-review).

Then the AGENT does the judgment (this is why no API key is needed):
1. **Review flagged names** — compare full names manually.
2. **Verify existence**: download OA PDFs for the usable pool; search the full
   text for the applicant's surname / cited-title fragments. ~5% of indexed
   citations are false positives — never cite a citation you haven't seen.
3. **Score depth of use** (HOW > WHO): implemented / compared-favorably /
   utilized / verified are high-value; background/passing are near-worthless.
   Score 1-9 (9 = the cited work is an explicit analytical framework across
   sections; 5 = one dedicated sentence; 1-2 = grouped passing mention).
4. **Quarantine negative citations**: any context framing the work as limited,
   superseded, or among methods that "fail to..." — actively harmful, never use.
5. **Select a portfolio** of ~10: coverage across several cited papers and
   subfields, not just top scores. Record in `citations/selected.md` with the
   verbatim citing quote for each.
6. **Never emphasize citer prestige** — USCIS compares credentials and it
   backfires. An extensive citation from an unknown researcher beats a passing
   mention from a famous one.
7. **Recommender candidates**: authors of selected citing papers who could
   discuss ≥2 notable citations; U.S.-based preferred; no students.

Deliverable per selected example (for `citations/examples.md`): cited paper ·
citing paper (full citation) · article type · verbatim citing text · citing
article's objectives (3-4 sentences) · how and why the work was used (4-5
sentences ending with the function it served) · findings and relation (4-5
sentences). Plain officer-readable English, technical terms glossed.

## Canonical fact table

Maintain `case.json` as the single source of truth: every venue, year,
authorship position, citation count (+as-of date), award ratio, employment
term, entity fact. Every drafted artifact must match it exactly; recheck at
signature time (counts drift). Scan ALL case documents for contradictions.
