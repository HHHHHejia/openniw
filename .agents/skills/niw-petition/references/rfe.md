# RFE — Prevention (at filing) and Response (if one arrives)

## Twelve prevention rules (check EVERY case against these before assembly)

1. **Endeavor = executable project, not research area.** Six fields per
   project: need, scenario, implementation path, beneficiaries, quantifiable
   impact, means of execution. Never argue from field importance. Test every
   planned project against the Policy Manual's Prong-1 negative examples —
   BEFORE Stage III and again here; a match means reframe or cut:
   classroom teaching without broader implications · working in a shortage
   occupation, alone · consulting for a nationally-important occupation ·
   benefits to a specific employer alone, even one with a national
   footprint · the software engineer adapting employer code for various
   clients.
2. **No uncorroborated third-party claims.** Every factual claim about an
   entity binds to an exhibit or gets deleted. The officer will block-quote
   your best unsupported sentence back at you.
3. **Pre-empt "common among researchers".** Degrees/pubs/citations/reviews
   are baseline; include ≥1 differentiating item (implementation by others,
   inbound collaboration requests, investment, government interest, critical
   role attested first-hand). Pre-load the rebuttal: Prong 2 is not a
   comparative test.
4. **Authorship & honors: primary proof.** Highlight equal-contribution
   notations in the OFFICIAL published version. State award selectivity as a
   ratio. Anything an officer can derive from a public profile — derive it
   first, correctly. A public Scholar profile is an adverse-inference surface.
5. **Never expose a denominator.** "Participated in projects funded by
   [award]" + a first-hand contribution-quality attestation; never grantee,
   never ratios.
6. **Foreign affiliation ⇒ mandatory documentation**: proof of affiliation +
   where the work is physically performed ("remotely from the U.S.") + a
   resources answer ("standard computing infrastructure"). One theme, one
   U.S. delivery vehicle.
7. **Answer "benefits only your employer" affirmatively**: dissemination
   argument (publications, patents' disclosure, open source); decouple
   national significance from commercial scale.
8. **Build Prong 3 from facts**, covering all five balancing factors:
   impracticality, benefit despite available workers, urgency (distinct from
   importance), job creation, the self-employment factor.
9. **Run the citation pipeline at filing time** (see evidence.md).
10. **One canonical fact table** (case.json); validate every artifact; scan
    all documents including marketing materials for contradictions;
    re-validate letters at signature time.
11. **Date-classify every exhibit** vs the priority date; flag claims resting
    on nothing pre-filing.
12. **The endeavor sentence is frozen once filed** (see endeavor.md).

## Claim-verification log (run alongside the twelve rules at Stage V)

Extract every factual claim from every document (start from
documents/source-registry.md), verify each against its source, and log a
table: claim | source (exhibit / case.json / URL) | verified? | finding.
Severity: CRITICAL = contradicts the source (canonical example: "50K
monthly users" where the source says 50K total) · WARNING = unsupported —
REQUIRES SOURCE · INFO. The two most common failures get explicit passes:
dates consistent across ALL documents; titles consistent across resume, HR
letter, and forms. Close with a verdict line: READY / NEEDS FIXES / MAJOR
ISSUES. Approach with skepticism, not trust.

## If an RFE arrives

Read the letter and produce `rfe/response-plan.md`:
1. **Anatomy**: which prongs challenged; each deficiency quoted and
   classified (missing-corroboration / comparative-test error / ratio
   arithmetic / authorship misreading / foreign-venue-resources /
   employer-only-benefit / urgency-not-shown), plus its root cause (8):
   no evidence submitted · wrong evidence type · evidence too weak ·
   missing sub-element · legal misframing · factual gap · self-serving
   evidence only · stale/irrelevant evidence — the root cause dictates the
   fix. The RFE's "you may submit" bullets are a LITERAL checklist: answer
   every bullet with evidence or an explicit reason it does not apply.
2. **Officer errors to rebut** — factual misreadings and legal-standard
   errors, each with the rebuttal + the physical proof needed.
3. **Evidence plan** by the officer's own suggested categories; classify each
   item pre-filing / post-filing-as-continuation (name the pre-filing thread
   it continues) / not-worth-it.
4. **Supplemental Personal Statement** (6 sections): endeavor restated
   VERBATIM + firewall sentence ("This supplemental statement clarifies...
   does not replace or materially alter..."); future plans anchored to the
   original with start dates and means of execution; broader implications;
   past accomplishments and interest; U.S. employment plans
   (benefit-beyond-employer + dissemination); references weighted toward
   U.S. government sources.
5. **Letters plan** — each letter described by the specific RFE finding it
   rebuts. Factual testimonials (employer/investor) are attestations, not
   expert opinions.
6. **Timeline** working back from the deadline: evidence for letters -8wk,
   drafting -5wk, first draft -3wk, exhibits assembled -2wk, delivery -1wk.
   Only ONE response submission is accepted, so everything ships at once —
   a partial response is permitted (8 CFR 103.2(b)(11)) but is adjudicated
   as a request for a decision on the record as-is.

Drafting the response: respond in the RFE's own ORDER, mirroring its
criterion headings; lead every point with NEW evidence ("We submit New
Exhibit X, which shows …") — the adjudicator already read the original
record and was not convinced; cite original + new exhibits together; every
point gets argument AND evidence, never re-argument alone (denials
increasingly recycle the RFE's own language against bare re-argument).

Never propose rewording the endeavor. Exhibit indexes should QUOTE the RFE
sentence each exhibit answers.

Sources: USCIS Policy Manual Vol. 6 Pt. F Ch. 5 (prong-1 negative examples,
verified live 2026-08-02); claim-log and RFE-response heuristics adapted
from juntoku9/claude_immigration_attorney (MIT).
