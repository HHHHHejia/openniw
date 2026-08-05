# Stage III — Drafting (PES → support letters → Petition Letter → index)

Order matters: the PES pins the frozen endeavor sentence; letters cite the
projects; the Petition Letter cites everything. Write each to `documents/`.
NEVER invent facts — insert `[TODO: what is needed]` for gaps. Every factual
claim about any entity (employer, lab, collaborator, customer) must cite an
exhibit or be DELETED (not softened): the officer will quote your most
impressive unsupported sentence back at you.

## Proposed Endeavor Statement (documents/pes.md, ~1,300 words)

First-person, signed, filed as an early exhibit; uses its own `(Reference N)`
numbering with a List of References. Outline:
1. Title "Proposed Endeavor & Future Plans in the Field" + date placeholder
   "[Please insert date of signature in MM/DD/YYYY format]"
2. §1 "My proposed endeavor is to [FROZEN SENTENCE, first person]."
3. §2 National-interest alignment: three "policy hook → my contribution"
   pairs, each `(Reference N)`. Research, verify (currency rule: no dead
   EOs), and rank the hooks per `national-importance-sources.md`. Weight
   references toward U.S. GOVERNMENT sources (agency data, statutes, federal
   reports); a market-size figure may appear but never carries the argument
   alone.
4. §3 Planned projects — 2-3 bullets, each rigidly: (a) bold gerund title;
   (b) goal with technical specifics; (c) U.S. beneficiaries/domains;
   (d) explicit linkage "This work directly supports my proposed endeavor,
   as I am ..."; (e) timeline + institution (past tense if started);
   (f) means of execution (funding/collaborators/infrastructure — "conducted
   remotely from the U.S. on standard computing infrastructure" where true).
5. §4 Employment as vehicle + the portability disclaimer (verbatim pattern):
   "my proposed endeavor is my overarching goal for my research career, and
   it will not change regardless of where I am employed... my ability to
   pursue my proposed endeavor is in no way limited to any one employer or
   role." (This appears twice: opening and closing.)
6. §5 Current role: title, start, salary, benefits, duties; if
   industry-employed, characterize ≥50% of the work as research.
7. §6 Employer's national significance — every claim exhibit-backed; include
   the dissemination argument (publications, patents' public disclosure, open
   source) and decouple national significance from commercial scale.
8. §7 Secondary affiliations with physical-location + resources answers.
9. §8 Closing re-emphasis + dissemination plan. Signature block with "do not
   sign until instructed". List of References.

## Petition Letter (documents/petition-letter.md, ~5,000 words)

Front matter: date, USCIS lockbox address, RE block (Petitioner/Beneficiary,
I-140, INA §203(b)(2)(B) NIW), opening invoking Matter of Dhanasar, a./b./c./d.
roadmap. Then four sections:

**I. Advanced degree** — one paragraph, two sentences, cites diploma exhibit.

**II. Prong 1 (substantial merit & national importance)** — one paragraph per
module, each anchored to exhibits: endeavor declaration (cites PES) · policy
alignment with named federal frameworks · concrete projects + federal
standards · national economy (only with real data) · employer-independence ·
federal R&D priorities · Critical & Emerging Technologies mapping ·
open-source metrics · funding ("participated in projects funded by...") ·
expert corroboration (quote 1-2 attributed sentences from signed support
letters where they exist) · Policy Manual restatement — quote the
"significant potential to broadly enhance societal welfare ... or to
contribute to the advancement of a valuable technology or field of study"
language; demonstrated POTENTIAL suffices · one-sentence close. CRITICAL:
argue from the SPECIFIC endeavor and concrete projects, never from field
importance. Source every policy/statistic module per
`national-importance-sources.md` (routing, SOURCE/QUOTE/CONNECTION format,
ranking, currency rule).

**III. Prong 2 (well positioned)** — the quantitative core: Dhanasar framing +
waiver disclaimer ("the petitioner's proposed endeavor is separate from the
proposed employment") · education/plan · peer-review (count + venue rankings)
· 3-5 contribution bullets (gerund-initial: problem → method → result) ·
publication tally by type × authorship role + venue-ranking bullets (Google
Scholar Metrics rank, CORE rank, or published acceptance rates) · total
citations + per-paper percentile bullets where data exists · citation
geography where the data supports it (N institutions across M countries;
name 2-3 prominent citing institutions with rankings — never invent the
numbers) · 3 independent citing-work bullets ("In a [YEAR] study in [VENUE],
[AUTHOR] et al. employed/incorporated/built upon the work to X, showing Y")
· awards with computed selectivity ratios · close restating the frozen
sentence verbatim.
State authorship positions explicitly. Prong 2 is NOT a comparative test —
note that once. Never expose diminishing denominators/ratios.

Walk the Policy Manual's well-positioned evidence list as a checklist —
every item that exists goes in; applicable gaps get flagged to the user:
degrees/licenses/certifications · patents/trademarks/copyrights · published
articles/media about the person's work · citation-history documentation, or
excerpts showing positive discourse around / adoption of the work ·
evidence of influence on the field · a U.S. continuation plan ·
correspondence from prospective customers, users, or investors · feasible
financial-support plans/models · U.S. investment (VC/angel/accelerator,
amounts appropriate to the endeavor) · contracts/agreements/licenses ·
letters from government or quasi-governmental entities · government
awards/grants/non-monetary support · evidence of others using the work
(contracts using the person's products; technology others use; significant
patents/licenses with adoption).¹

¹ Policy Manual, Vol. 6 Pt. F Ch. 5: letters "may be persuasive when they
are from experts … and are supported by other independent evidence";
"unsubstantiated claims would not meet the petitioner's burden of proof."

**IV. Prong 3 (on balance)** — seven short paragraphs: recap · benefits
outweigh labor-cert interests · urgency (DISTINCT from importance — tie to
short-term national priorities) · bridge · impracticality of labor cert ·
minimum-requirements argument · "clearly satisfies the third prong."
When the applicant has an advanced STEM degree (especially a PhD) AND the
endeavor furthers a critical and emerging technology, add the Policy Manual
strong-positive-factor paragraph (STEM PhD + critical technology + well
positioned = expressly a strong positive factor). Entrepreneurs: concrete
job-creation/revenue potential only with real supporting data.

**INDEX OF EXHIBITS** (also saved standalone as documents/exhibit-index.md)
— three groups: Academic and Professional Background /
Publications and Citations / Other. Positional numbering; publications one
exhibit per paper, published first then preprints; a/b sub-letters pair
applicant-proof with legitimizing context. Inline citations `(Exhibit N)` /
`(Exhibits N–M)` (en-dash), sentence-final. Legal authorities (Dhanasar,
Policy Manual) in FOOTNOTES only.

**Source registry** (documents/source-registry.md, printable) — build it
WHILE drafting, not after; it feeds Stage V's claim-verification log
(rfe.md) and any later RFE response. Every factual claim gets a line:
claim → exhibit number, or URL + verbatim quote + retrieval date for web
facts. LOAD-BEARING claims — what the petition letter argues from, anything
about a third-party entity, anything asserting impact — get the full row.
Two tables, and the headings are a contract: `openniw registry` parses them.

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
  claim. This is the check exhibit-binding alone misses: an employer letter
  IS an exhibit, so the claim binds — and still reads as an interested party
  vouching for itself, which is exactly what real RFEs block-quote back.
- **measure** — impact claims only: the number and its as-of date. Blank
  elsewhere; never manufacture precision to fill a cell.
- **gap** — what is still missing for the claim to stand ([TODO] text).

Check each new row against those already written: the same fact carrying a
different number or date is a contradiction to fix NOW, not at Stage V.

## Every generated document carries a draft header

The first lines of `documents/petition-letter.md`, every support letter, the
statement, and any RFE response draft — before the date line, so it survives
copy-paste but sits outside the letter's own body:

```
SELF-HELP DRAFT — NOT ATTORNEY-REVIEWED
Generated by open-source software from user-provided information. An editable
draft for independent review. OpenNIW does not determine eligibility, provide
representation, or certify that any argument or evidence satisfies a legal
standard. Delete this header before filing.
```

Put it there once and nowhere else. Do NOT sprinkle disclaimers through the
body — a petition letter interrupted by warnings reads as an unserious
filing, which serves the user badly. The header, the preview, and your own
message when you hand the draft over are the right places.

## Quality bars (lint before showing the user)

Consistent honorific throughout · endeavor sentence verbatim at every
occurrence · no [TODO] left at finalization · no dangling template
instructions · every entity claim exhibit-bound · no field-level-importance
arguments standing alone · all numbers match case.json · every claim has a
source-registry line · every load-bearing claim names an independent
verifier or says why none exists.

Sources: USCIS Policy Manual Vol. 6 Pt. F Ch. 5 (prong-2 evidence list +
letters language, verified live 2026-08-02); source-registry packaging idea
adapted from juntoku9/claude_immigration_attorney (MIT).
