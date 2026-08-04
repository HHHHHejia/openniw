# RFE prevention (at filing)

O-1 RFEs are common but survivable: practitioner-compiled figures from
USCIS data (immi-usa, FY2025) put the O RFE rate near 20% and the
OVERALL O approval rate above 90% — an overall rate across all filings,
NOT a post-RFE outcome rate and not any individual case's odds;
directional only. An RFE is a curable defect list, not a denial.
Prevention first; if a notice has already arrived, the response workflow
lives in `references/rfe-response.md`.

## Twelve prevention rules (check EVERY case against these before assembly)

1. **Itinerary specificity.** Every engagement has dates, employer legal
   name + address, venue + address, and a contract exhibit; the events
   cover the whole requested validity; zero speculative or contingent
   rows. The #1 O-1 trap.
2. **Agent authority on paper.** Multi-employer filings carry a signed
   authorization from EACH employer and contracts predating filing; no
   circular founder-as-agent setups without real third-party engagements.
3. **Consultation validity.** Qualified signer (expertise at the relevant
   intersection), explicit no-peer-group/no-union statement for
   union-less fields, zero conflicts of interest (never an investor,
   advisor, or employee), watermarked original where issued.
4. **Ability-vs-role match.** Every duty of the U.S. role maps to the
   frozen field label; acclaim-as-X + role-as-Y is an RFE even with
   perfect criteria.
5. **Mandatory documentary layer complete.** Contract or oral-agreement
   summary + event explanation with dates + consultation — each missing
   item is an RFE independent of the criteria.
6. **Criterion sub-elements each evidenced.** Awards: received AND
   recognized AND for excellence; memberships: outstanding-achievement
   AND judged-by-experts; published material: about-the-person AND major
   outlet; judging: completed, not invited. Argue 3-4 strong criteria;
   withdraw weak ones now, not after an RFE.
7. **No uncorroborated third-party claims.** Every factual claim about an
   entity binds to an exhibit or gets deleted; no adjective without its
   sourced fact.
8. **Founder governance real on paper.** Separate legal entity, employment
   agreement, board with independent oversight, "could be fired" answer;
   no evidence dated entirely in the weeks before filing.
9. **Original-contributions criterion shows others' reliance** — run the
   citation pipeline at filing time; adoption beyond the applicant's own
   employer, verified in full text.
10. **One canonical fact table** (case.json); validate every artifact;
    re-validate letters at signature time; dates and wages identical
    across I-129, contract, itinerary, and support letter.
11. **Date-class every exhibit.** Eligibility is judged at filing;
    acclaim must read as sustained to the present, not one early spike.
12. **The frame is frozen once filed.** Petitioner, role, or terms
    changes after filing are material changes → amended petition, never
    a quiet rewording in the response.

## Claim-verification log (run alongside the twelve rules before assembly)

Extract every factual claim from every document (start from
`documents/source-registry.md`), verify each against its source, and log a
table: claim | source (exhibit / case.json / URL) | verified? | finding.
Severity: CRITICAL = contradicts the source (canonical example: "50K
monthly users" where the source says 50K total) · WARNING = unsupported —
REQUIRES SOURCE · INFO. A verified source is not the end of it: for every
load-bearing claim read the registry's independent-verifier cell too — a
criterion resting only on the petitioner's own support letter is the
employer vouching for its own hire, and USCIS says so in the RFE. The
three most common failures get explicit passes: dates and wages identical
across I-129, contract, itinerary and support letter; the field label
identical everywhere; the beneficiary's title identical across CV, letters
and forms. Close with a verdict line: READY / NEEDS FIXES / MAJOR ISSUES.
Approach with skepticism, not trust.

## If a notice has already arrived

Stop here and switch to `references/rfe-response.md` — the R1–R7 response
workflow (intake and emergency reverse-build of an externally filed case,
diagnosis against USCIS's own O-1A RFE template, the evidence matrix and
supply loop, letters, the petitioner's supplemental letter, assembly, and
the petitioner hand-off). The twelve rules above come back one last time
as a red-team pass over the response package before it ships.

Sources: RFE taxonomy from practitioner guides (immi-usa.com, tukki.ai,
compassvisas.com) and USCIS Policy Manual Vol. 2 Part M Ch. 8; prevention
checklist patterns adapted from juntoku9/claude_immigration_attorney
(MIT); rate figures are practitioner-compiled from USCIS data —
directional only.
