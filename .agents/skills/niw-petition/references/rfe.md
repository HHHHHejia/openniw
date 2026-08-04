# RFE Prevention — run at filing time (Stage V red team)

A notice has already arrived? Read `rfe-response.md` FIRST (R1–R7,
deadline-driven), then come back here for the pre-ship red team. The rules
below are the FILING-side checks; at RFE time they work twice — as a
diagnostic (each officer finding usually maps to a rule that was not satisfied
when the case was filed) and, at R6, as the quality gate the assembled
response package must clear before it is printed.

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
REQUIRES SOURCE · INFO. A verified source is not the end of it: for every
load-bearing claim, read the registry's independent-verifier cell too. An
interested party (employer, investor, the applicant) vouching for a claim
is SELF-SERVING ONLY — a real RFE root cause, and far cheaper to cure with
one independent attestation now than to answer under a deadline later. The two most common failures get explicit passes:
dates consistent across ALL documents; titles consistent across resume, HR
letter, and forms. Close with a verdict line: READY / NEEDS FIXES / MAJOR
ISSUES. Approach with skepticism, not trust.

## The three prevention habits that make an RFE survivable later

Filing-side work that pays off only if an RFE arrives — do it now, not then:
- **Date-class every exhibit as you file it** (rule 11). At RFE time the
  at-time-of-filing doctrine decides what may still be used, and a case whose
  exhibits were never date-classed has to be re-audited under deadline.
- **Keep `documents/source-registry.md` current** (drafting.md). It becomes the
  rebuttal-ammunition list: officer error → corrective fact → the exhibit.
- **Ask the government-connections question at filing**, not only at RFE time:
  letters from governmental or quasi-governmental entities are the class
  practitioners describe as the only one able to support all three prongs (an
  attorney-practice observation, not a USCIS rule; details in
  `rfe-response.md`).

Sources: USCIS Policy Manual Vol. 6 Pt. F Ch. 5 (prong-1 negative examples,
verified live 2026-08-02); claim-log and RFE-response heuristics adapted
from juntoku9/claude_immigration_attorney (MIT).
