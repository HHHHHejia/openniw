# Stage II·b — Evidence Collection & The Citation Pipeline

Maintain `evidence/checklist.md` as a ledger: one line per item with
status (`suggested | needed | provided | na`), organized by claimed
criterion; files live in `evidence/exhibits/` — anything handed over from
elsewhere gets COPIED there immediately (standing rule 4). Every claim a
letter makes must be shadowed by an objective exhibit. Tiers: Tier 1
independent third-party records (institutional records, gatekept media,
peer-reviewed publications, established awards) > Tier 2 solicited
third-party (independent expert/organization letters) > Tier 3
related-party (colleague letters, employer material) > Tier 4
self-generated (CV, screenshots). Each claimed criterion needs ≥1
Tier-1/2 anchor.

## Criterion-by-criterion: what qualifies, what proves it, the traps

**(i) Prizes/awards** — sub-elements: the person RECEIVED it (team awards
count if named/on the podium — Oct 2024 policy) · nationally or
internationally recognized · for excellence, not participation. Evidence:
notice naming the person + the award's public page + selection criteria
and selectivity (N of M, eligibility pool, judges, past winners).
Dissertation and best-paper awards from well-known institutions can
qualify. TRAP — the student award: university-internal prizes, travel
grants, and scholarships judged only against classmates fail "national";
research grants read as funding future work, not honoring past
excellence — argue them under (v)/(viii).

**(ii) Membership** — sub-elements: membership held (past membership
counts — Oct 2024) · the association REQUIRES outstanding achievements ·
judged by recognized national/international experts. Prove from bylaws/
admission criteria, never from the applicant's own accomplishments.
Fellow grades judged by expert panels (IEEE Fellow-class, AI-society
fellows) reliably work. TRAP — pay-to-join: memberships based
on education, experience, dues, or employment (ordinary ACM/AAAS/Sigma Xi,
unions/guilds) reliably fail; IEEE Senior Member is adjudicated
inconsistently — document the elevation-panel review, never load-bearing.

**(iii) Published material about the person** — sub-elements: material is
about the person and their work (need NOT demonstrate the work's value —
Oct 2024) · in professional/major trade publications or major media ·
with title, date, author + certified translation. Team-focused coverage
counts if the person is named in connection with the work. Evidence: the
article + an outlet-stature page (circulation/readership). TRAP —
about-the-work-not-person: coverage that never names the applicant,
employer/university press releases (institutional stake), paid or
"contributor" placements, and passing mentions all fail; most bench
scientists cannot claim this criterion — don't force it.

**(iv) Judging** — sub-elements: actually judged (not merely invited) ·
work of others · same or allied field. Qualifying: journal peer review,
conference program-committee review, PhD dissertation committees,
grant-program review. Evidence: the full email trail per review
(invitation → assignment → completion), an editor's letter quantifying
the record, plus VENUE-PRESTIGE framing (impact factor, acceptance rate) —
thank-you screenshots without venue context are the classic RFE. TRAP —
uncompleted reviews count for nothing; judging student/high-school work
or sitting on panels alongside non-experts undermines final merits.

**(v) Original contributions of MAJOR SIGNIFICANCE** — the highest-failure
criterion; budget the most evidence. Sub-elements: original · of major
significance to the field (not just the employer). The working
architecture is a triangle: expert letters (interpretation) + citation
analytics (independent engagement) + adoption evidence (named external
groups using the method/dataset/tool, clinical/industrial adoption,
standards, practiced patents, replications). Structure around 2-3 NAMED
contributions, each with its own per-article citation counts,
citing-institution list, and verbatim citing quotes — aggregate totals
were expressly rejected in 2026 AAO decisions when the flagship articles
had 0-15 citations each. Letters must document what others actually DID
differently; novelty assertions and future speculation are discounted.

**(vi) Scholarly articles** — easy at Step 1 for any publishing academic
(peer-reviewed journals AND published proceedings of recognized
conferences qualify); worthless at Step 2 unless framed comparatively:
venue acceptance rates, impact factor/rank, CORE tier, authorship
positions, a peer-relative citation benchmark — never bare counts
("postdocs are expected to publish" is Kazarian itself). Exhibit: official
published version, first 3-5 pages, name highlighted, venue+year visible.
TRAP — predatory venues: any pay-to-publish journal or purchased review is
an affirmative liability (2025-26 revocation wave); exclude before drafting.

**(viii) Leading or critical role** — sub-elements: role was leading
(title + duties) OR critical (outcome-level consequence — performance,
not title) · for an organization or distinct division WITH a distinguished
reputation (rankings, government research grants, funding scale, media).
Qualifying shapes: senior position in a distinguished department; PI or
named investigator on a merit-based government award (SBIR-class);
founder/co-founder or IP contributor to a well-funded startup; core
maintainer of a widely adopted tool; leading a named work package in a
multi-institution project. Evidence: org letter from firsthand knowledge
+ outcome data + the org's distinction proved externally. TRAP —
"critical role in my PI's lab" reads as expected duties; a role letter
that reads like a job description draws "not critical"/"not distinguished".

**(ix) High salary** — total compensation significantly above others in
the field: W-2/pay statements (or a credible signed offer — "has
commanded" includes prospective salary) against ≥2 independent sources
(BLS OEWS, OFLC wage levels) for the right occupation code and location;
practitioner convention is ≥90th percentile. Founder equity/funding
context counts (comparable evidence). TRAP — academic pay bands: postdocs
and most faculty cannot clear the percentile — skip, don't stretch;
parity with same-rank peers fails (compare to the field's top).

**(vii) Artistic exhibitions and (x) performing-arts commercial success**
— usually `na` for researchers. (vii): artistic work only (Oct 2024),
non-artistic showcases only as properly supported comparable evidence;
(x): volume of box-office/sales receipts vs others, mere releases fail.

## Per-type evidence specs (all criteria)

Publications from `sources/papers/` (chase gaps now) · citation record:
Google Scholar ONLY, profile printed to PDF logged-out · venue standing:
Scholar Metrics/CORE page per venue, published acceptance rates · awards:
notice + public page + selectivity ratio · media: article + outlet-stature
evidence · screenshots: full URL visible, logged out, dated · EVERY
foreign-language document: full English translation + translator's signed
certification · recommender CVs: max 5 pages each. Date-class every
exhibit: eligibility is judged AS OF the filing date, post-filing evidence
is irrelevant even on appeal; tag each exhibit's YEAR — "sustained" wants
recognition across ≥2-3 distinct career periods (an all-last-2-years
record is a known dismissal pattern).

## The citation pipeline (feeds criteria (v) and (vi))

Run `openniw harvest "Title 1" ...` (fallback
`scripts/harvest_citations.py`) — pulls every citing paper from OpenAlex
with authors/venue/OA-PDF links, screening independence (exact-name ⇒
dependent; family+initial collision ⇒ conservatively dependent + flagged;
family-only ⇒ independent + flagged) and published-only. Then the AGENT
does the judgment:
1. Review flagged names manually.
2. Verify existence: download OA PDFs, search the full text for the
   applicant's surname/cited title — never cite a citation you haven't
   seen (~5% of indexed citations are false positives).
3. Score depth of use 1-9 (implemented/compared/utilized ≫ background
   mention); per-article depth for flagship contributions beats aggregates.
4. Quarantine negative citations (work framed as limited/superseded).
5. Select a portfolio of ~10 with coverage across papers and subfields;
   verbatim citing quotes go in `citations/selected.md`; for browser
   selection write `citations/scored.json`, open `openniw ui citations`.
6. Never emphasize citer prestige — depth of use beats fame.
7. Recommender candidates: independent authors of selected citing papers.

Deliverable per selected example (`citations/examples.md`): cited paper ·
citing paper (full citation) · verbatim citing text · citing article's
objective · how/why the work was used · findings — officer-readable English.

## Canonical fact table

Maintain `case.json` as the single source of truth: field-of-endeavor
label, venues, years, authorship positions, citation counts (+as-of
dates), award ratios, membership grades, salary figures, employment
terms. Every drafted artifact must match it exactly; re-check at
signature time (counts drift) and scan ALL case documents for
contradictions — names, dates, titles, amounts, exhibit numbers.

Sources: USCIS Policy Manual Vol. 6 Part F Ch. 2 (criterion
considerations; PA-2024-24) via uscis.gov; 8 CFR 204.5(h)(3)-(4); 2026
AAO dismissal patterns via millermayer.com and greencard.writewing.in;
tiers/sub-elements adapted from juntoku9/claude_immigration_attorney (MIT).
