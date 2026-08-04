# Stage III — Drafting (statement → support letters → Petition Letter → index)

Order matters: the statement pins the frozen field definition and intent
scope; letters cover their assigned criteria; the Petition Letter cites
everything. Write each to `documents/`. NEVER invent facts — insert
`[TODO: what is needed]` for gaps. Every factual claim about any entity
(employer, venue, award body, organization) must cite an exhibit or be
DELETED (not softened): the officer will quote your most impressive
unsupported sentence back at you.

## Intent-to-continue-work statement (documents/statement.md, ~1 page)

The 8 CFR 204.5(h)(5) vehicle for a self-petitioner: first-person, signed,
filed as its own package item. Structure:
1. Title "Statement of Intent to Continue Work in the Area of
   Extraordinary Ability" + date placeholder "[insert date of signature]".
2. Who I am + the frozen field definition VERBATIM.
3. Concrete plans: ongoing projects and collaborations continuing in the
   U.S., named position or realistic pipeline (interviews, offers,
   prearranged commitments), employer-independent framing — the work
   continues regardless of any single employer.
4. Prospective U.S. benefit (INA 203(b)(1)(A)(iii)): the frozen hook,
   expanded to one paragraph of concrete mechanism — who in the U.S. uses
   or gains from the continued work; where true, note how permanent
   residence expands the work (e.g., eligibility for federal funding
   restricted to citizens/permanent residents).
5. Signature block with "do not sign until instructed".
Employer letters or contracts, where they exist, are attached as exhibits
supplementing (never replacing) the statement.

## Petition Letter (documents/petition-letter.md, ~4,000-6,000 words)

An explicit Kazarian two-step brief. Front matter: date, USCIS lockbox
address, RE block (Petitioner/Beneficiary — same person, Form I-140,
Classification: INA §203(b)(1)(A) Alien of Extraordinary Ability), opening
that cites 8 CFR 204.5(h)(1) (self-petition) and (h)(5) (no job offer or
labor certification), states the frozen field definition, and enumerates
up front exactly which N≥3 criteria the petition satisfies with internal
section references. Then:

**§1 Summary of achievements** — one page: short bio, the field
definition, then one paragraph per claimed criterion previewing its
strongest numbers. An officer who reads only this page should already see
the whole case.

**§2 One section per claimed criterion** (Step 1) — each section rigidly:
(a) the criterion's regulatory text quoted with its (h)(3) cite;
(b) the argument, decomposed by sub-element (evidence.md), every
sub-element affirmatively covered; (c) exhibit-bound evidence. Craft
rules:
- Subsection headlines are themselves claims ("Evidence of original
  contribution: developed the benchmark now used by N independent
  groups"), never generic headers.
- Paragraph contract: claim → sourced entity facts → tie to the legal
  standard → numbers with exhibit cites → close. No paragraph without at
  least one specific sourced number; replace every stacked adjective with
  a sourced fact.
- Scholarly articles argue in three moves: volume → venue quality
  (acceptance rates, rankings) → peer-relative citation benchmark.
- Original contributions: 2-3 named contributions, each with per-article
  citations, citing institutions, and 1-2 verbatim citing quotes; quote
  1-2 attributed sentences from signed support letters where they exist —
  always next to the documentary corroboration, never alone.
- End each section: "This evidence satisfies 8 CFR 204.5(h)(3)([the
  criterion's roman numeral]) because ..." — one sentence.

**§3 FINAL MERITS DETERMINATION** (Step 2 — the section most DIY petitions
omit, and where petitions die). Two subsections mapping 1:1 to the legal
tests:
- **"One of that small percentage at the very top of the field"**
  ((h)(2)): explicit comparison against the field's elite, not average
  practitioners — citation percentile within the frozen field, venue-rank
  standing, and the Policy Manual positive factors that apply: highly
  ranked journals (impact factor, senior/first authorship), high citation
  rate / h-index FOR THE FIELD (state the methodology; early-career
  beneficiaries are excused heavy counts per the Manual), employment or
  research experience at leading institutions (Carnegie R1/R2 or
  comparable foreign / QS-ranked), unsolicited invitations to speak at
  recognized conferences, named investigator on a peer-reviewed
  competitively funded U.S. government grant. Provide CONTEXT for every
  factor — why this ranking or percentile matters in this field.
- **"Sustained national or international acclaim"**: a timeline narrative
  ("From [year] to present...") showing recognition across ≥2-3 distinct
  career periods; breadth (independent validators across institutions and
  countries); continuity/recency (citations in the last 6-12 months,
  recent invited talks, current roles). "Sustained" has no minimum years
  and no age limit — but an all-recent-burst record must be argued as
  trajectory + current standing, honestly.
Weave, don't re-list: this section connects the criterion sections into
one narrative and may draw on ALL evidence, including items that fit no
criterion.

**§4 Intent to continue work in the area of expertise** — short section
citing the signed statement (exhibit) and any employer letters/contracts.
USCIS can RFE this even when all criteria are met — never skip it.

**§5 Substantial prospective benefit to the United States** — one to two
paragraphs keyed to INA 203(b)(1)(A)(iii), citing the statement and any
adoption/dissemination evidence. The standard is broad (*Matter of
Price*); concrete and truthful beats grandiose.

**§6 Conclusion** — restates that the beneficiary meets INA 203(b)(1)(A)
and 8 CFR 204.5(h), one-sentence recap per claimed criterion, requests
approval.

**INDEX OF EXHIBITS** (also saved standalone as documents/exhibit-index.md)
— groups: Identity and Status / Statement and Letters / then one group per
claimed criterion in argued order / Background. Positional numbering;
publications one exhibit per paper; a/b sub-letters pair applicant-proof
with legitimizing context (award page + selectivity page). Inline
citations `(Exhibit N)` / `(Exhibits N–M)` (en-dash), sentence-final.
Legal authorities (Kazarian, Policy Manual) in FOOTNOTES only.

**Source registry** (documents/source-registry.md, printable) — build it
WHILE drafting, not after; it feeds Stage V's claim-verification log
(rfe.md) and any later RFE response. Every factual claim gets a line:
claim → exhibit number, or URL + verbatim quote + retrieval date for web
facts. LOAD-BEARING claims — what the letter argues a criterion from,
anything about a third-party entity, anything asserting impact — get the
full row. Two tables, and the headings are a contract: `openniw registry`
parses them.

```markdown
## Load-bearing claims
| claim | source | locator | independent verifier | measure | gap |
|---|---|---|---|---|---|

## Supporting facts
| claim | source |
|---|---|
```

- **locator** — exhibit + page + paragraph ("Ex. 12 at 3, ¶2"); an officer
  who cannot find the proof has not been given it.
- **independent verifier** — who attests this OTHER than the applicant and
  anyone with a stake in the outcome (employer, investor, co-founder, the
  applicant's own statement). Write "NONE — self-serving" when that is the
  truth, because the officer will; then get one before filing, or cut the
  claim. Exhibit-binding alone misses this: an employer letter IS an
  exhibit, so the claim binds — and still reads as an interested party
  vouching for itself. Final-merits findings turn on exactly this.
- **measure** — impact claims only: the number and its as-of date. Blank
  elsewhere; never manufacture precision to fill a cell.
- **gap** — what is still missing for the claim to stand ([TODO] text).

Check each new row against those already written: the same fact carrying a
different number or date is a contradiction to fix NOW, not at Stage V.

## Quality bars (lint before showing the user)

Field-of-endeavor phrase verbatim at every occurrence · claimed-criteria
list identical everywhere (letter, statement, worksheet) · every
sub-element of every claimed criterion affirmatively argued · a Final
Merits section exists and addresses BOTH tests · no aggregate-only
citation claims (per-article counts present for flagship works) · every
entity claim exhibit-bound · no speculative language (potential/possible/
may) about the work's significance · no [TODO] left at finalization · no
dangling template instructions · consistent honorific · all numbers match
case.json · every claim has a source-registry line · every load-bearing
claim names an independent verifier or says why none exists.

Sources: USCIS Policy Manual Vol. 6 Part F Ch. 2 (two-step, positive
factors); Kazarian v. USCIS, 596 F.3d 1115 (9th Cir. 2010); 8 CFR
204.5(h); letter architecture informed by public approved self-petitions
(razvanmarinescu/EB1A, Ryan-Rhys/EB1A — structure only, no text reused);
section pattern, paragraph contract and source-registry packaging idea
adapted from juntoku9/claude_immigration_attorney (MIT).
