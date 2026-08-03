# Stage II·b — Evidence Collection (8 criteria + the O-1 documentary layer)

Maintain `evidence/checklist.md` as a ledger: one line per item with status
(`suggested | needed | provided | na`), and `evidence/exhibits/` for files.
Exhibit files the user hands over from anywhere else get COPIED into
`evidence/exhibits/` immediately (standing rule 4). Objective evidence
beats subjective: every claim a letter makes must be shadowed by an
objective exhibit. Build the exhibit index FROM the claims.

**Numbering discipline**: use the REGULATORY order of 8 CFR
214.2(o)(3)(iii)(B) below (some published guides shuffle it — 4 is
judging, 5 is original contributions). Argue the 3-4 strongest criteria
only: three strong criteria beat six weak ones, and every weak criterion
argued is an RFE surface. Each criterion needs at least one independent
third-party anchor (official record, major media, published paper,
established award) — a criterion resting only on colleague letters and
self-generated material fails.

## The 8 O-1A criteria — what to collect per criterion

1. **Prizes/awards for excellence** — two-part test: received it (named
   recipient — team awards count if named; "being on a list" is not an
   award), and nationally/internationally recognized for excellence.
   Collect: award notice + public page + selection criteria + selectivity
   facts (grantor, founding year, N winners of M entrants, judge
   credentials, geographic reach). Dissertation awards, competitive
   fellowships, and conference best-paper awards can qualify (Policy
   Manual examples); grants framed as nationally competitive awards work
   (NSF/NIH-class). VC investment as an "award" must be affirmatively
   argued (USCIS default: funding funds the future, it doesn't honor the
   past) — selection ratio + published criteria or skip it.
2. **Memberships requiring outstanding achievement** — judged by
   recognized national/international experts, assessed at the tier held
   (IEEE Fellow and AAAI Fellow are USCIS's own examples). Excluded:
   fee/subscription-based, education/experience-based, job-required
   memberships. Collect: bylaws/criteria page, acceptance-rate or member
   counts, who elects and their credentials, the admission letter.
3. **Published material ABOUT the beneficiary** — about their work (they
   or their documented role must be named; team coverage counts), in
   professional/major trade publications or major media, with title, date,
   author visible; include circulation/readership context. Press releases
   and paid/advertorial placements don't count; material BY the applicant
   belongs under criterion 6. Foreign-language items need certified
   translation + original.
4. **Judging the work of others** — proof of COMPLETED review, not
   invitation alone: per-review email trails (invitation → assignment →
   completion) or reviewer-dashboard records; dissertation committees,
   conference program committees, grant-panel service (government funding
   programs are a Policy Manual example) count. Lead with the 2-3 most
   prestigious instances in full, then a tally. Diversify organizers.
5. **Original contributions of major significance** — originality alone is
   insufficient; significance must be shown by others' reliance: citation
   record relative to the field, published material about the work,
   patents/licenses WITH adoption or commercialization, software/data
   repository contributions with impact evidence, expert letters with
   corroboration, an interested government-agency letter. Impact must
   extend beyond the applicant's own employer. This is the most-contested
   criterion — feed it with the citation pipeline below.
6. **Authorship of scholarly articles** — the published record itself: the
   criterion needs NO citation minimum (citations argue criterion 5 and
   totality); peer-reviewed conference proceedings count. Collect: the
   PDFs auto-downloaded to `sources/papers/` in Stage I (official
   published version, first 3-5 pages per exhibit, name highlighted,
   venue+year visible), venue rankings/acceptance rates. Pay-to-publish
   venues technically qualify but damage the totality read.
7. **Critical/essential capacity for distinguished organizations** —
   duties and performance, not title; the org's distinguished reputation
   needs EXTERNAL evidence (rankings, funding, major clients, press — for
   a startup: significant funding from government, VC, or angels
   commensurate with stage). Direct employment not required. Examples that
   work: named/principal investigator on a merit-based government award,
   founder who contributed the core IP, role attested first-hand by a
   director/PI with an org chart.
8. **High salary or other remuneration — past OR prospective** ("has
   commanded or WILL command"; a signed offer letter counts — key for
   founders). Collect: contracts/W-2s/offer letter + at least two
   independent comparators (BLS OEWS for the SOC code and location, plus
   a market survey); overseas salaries compare against LOCAL wage data,
   never USD conversion. Equity: vested RSUs on W-2s count cleanly;
   unexercised options are weak — high-value equity is usually argued as
   COMPARABLE evidence instead (ownership % × valuation, two independent
   comparators; a SAFE cap is not a 409A valuation — explain why the
   number reflects real value). A startup's funding also underwrites the
   credibility of a prospective salary.

**Comparable evidence** (criterion-by-criterion): explain (a) why a listed
criterion is "not readily applicable" to the occupation (it need not be
entirely inapplicable) and (b) why the substitute evidence is comparable —
a detailed, credible statement suffices. Still need 3 criteria total.

## The O-1-specific documentary layer (mandatory, criteria aside)

Missing any of these is an RFE independent of the criteria
(8 CFR 214.2(o)(2)(ii)):
- **Contract**: copies of written contracts between petitioner and
  beneficiary — or the summary of the oral agreement (terms offered +
  accepted; supporting emails; need not be signed by both). Founders: the
  employment agreement; consultants: client contracts / deal memos.
- **Event explanation + itinerary**: nature of the events/activities,
  begin/end dates; itinerary doc per petition-frame.md (mandatory when
  multiple locations/employers).
- **Consultation package** (to send the signer): draft advisory-opinion
  scaffold (drafting.md), the applicant's CV, the frozen field label +
  role description, 3-5 key exhibits. Track request → received in the
  ledger; file the watermarked original if the org uses watermarks.
- **Petitioner documents**: structure-dependent per petition-frame.md
  (corporate/governance package, or agent authorizations + per-employer
  contracts, or employer letter). Ability-to-pay is NOT among the O-1
  initial-evidence requirements (8 CFR 214.2(o)(2)(ii) lists contract,
  event explanation + dates, itinerary, consultation — contrast the
  I-140's 8 CFR 204.5(g)(2)); clarity of the offered terms is what
  matters.
- Identity/status set: passport bio page, current I-94 + status documents
  (for COS), degree(s), CV. Certified English translation + translator's
  certification for EVERY foreign-language document.
- Date-class every exhibit: eligibility is judged as of filing; acclaim
  must read as sustained up to now, not a single early-career spike.

## The citation pipeline (feeds criteria 5 and 6)

Run `scripts/harvest_citations.py "Title 1" "Title 2" ...` (or
`openniw harvest`) — it pulls every citing paper from OpenAlex with
authors/venue/OA-PDF links and screens independence (exact-name match ⇒
dependent; family+initial collision ⇒ conservatively dependent + flagged)
and published-only. Then the AGENT does the judgment:
1. Review flagged names manually.
2. Verify existence: download OA PDFs, search full text for the
   applicant's surname/title fragments — never cite a citation you
   haven't seen (~5% of indexed citations are false positives).
3. Score depth of use (HOW > WHO): implemented / compared-favorably /
   utilized are high-value; passing mentions near-worthless. 1-9 scale.
4. Quarantine negative citations (work framed as limited or superseded).
5. Select ~10 for the portfolio: coverage across papers and subfields.
   Write `citations/scored.json` and offer `openniw ui citations`; record
   picks with verbatim citing quotes in `citations/selected.md`, worked
   examples in `citations/examples.md` (cited paper · citing paper · how
   and why the work was used · function it served — officer-readable).
6. Never emphasize citer prestige — an extensive citation from an unknown
   researcher beats a passing mention from a famous one.
7. Expert-letter candidates: authors of selected citing papers
   (independent), plus the criterion-coverage needs in support-letters.md.

## Canonical fact table

Maintain `case.json` as the single source of truth: every venue, year,
authorship position, citation count (+as-of date), award ratio, salary
figure, employment term, petitioner entity fact. Every drafted artifact
must match it exactly; recheck at signature time (counts drift). Scan ALL
case documents for contradictions.

Sources: 8 CFR 214.2(o)(2)-(3) (eCFR); USCIS Policy Manual Vol. 2 Part M
Ch. 4 (criterion considerations) and Ch. 7 (contracts, consultations);
evidence-hierarchy and argument patterns adapted from
juntoku9/claude_immigration_attorney (MIT); STEM evidence menus: ifp.org
O-1A guide.
