# Stage III — Drafting (support letter → consultation → itinerary → letters → index)

Order matters: the support letter pins the frozen field label and role;
the consultation and expert letters echo them; the exhibit index cites
everything. Write each to `documents/`. NEVER invent facts — insert
`[TODO: what is needed]` for gaps. Every factual claim about any entity
(employer, award grantor, publication, investor) must cite an exhibit or
be DELETED (not softened): the officer will quote your most impressive
unsupported sentence back at you. Never write "prestigious", "renowned",
"leading" or any such adjective unless the next clause states the sourced
fact that earns it.

## Petitioner support letter (documents/support-letter.md, ~3,000-5,000 words)

Written in the PETITIONER's voice, signed by the petitioner's signatory —
this is the core persuasive document riding on the I-129.

Front matter: date, USCIS lockbox address placeholder, RE block
(Petitioner / Beneficiary / Classification: O-1A / Field: [frozen label]
/ Position: [title]), then:

1. **Opening** — who the petitioner is (one exhibit-backed paragraph:
   entity, what it does, funding/scale facts), the offered role, and the
   request: classify the Beneficiary as O-1A for [dates ≤3 years].
2. **Terms of employment** — title, duties (each mapped to the field
   label), wage, dates, location(s); cite the contract or oral-agreement
   summary exhibit. (Ability-to-pay is not an O-1 requirement; clarity of
   terms is.) Agent filings: summarize the itinerary and each employer's
   authorization here.
3. **Standard** — one short paragraph: extraordinary ability = "one of
   the small percentage who have arisen to the very top of the field",
   demonstrated by sustained acclaim; the Beneficiary satisfies [3-4
   named criteria] of 8 CFR 214.2(o)(3)(iii)(B). Cite the regulation and
   Policy Manual only — no Kazarian (that is EB-1A case law).
4. **Criterion-by-criterion argument** — one section per argued
   criterion, regulatory numbering, strongest first. Recipe per
   paragraph: open with the claim → sourced entity facts → tie to the
   criterion's legal text → specific numbers → tie back to the field
   label → close ("This [X] places the Beneficiary among..."). Cite
   `(Exhibit N)` sentence-finally. Repeat the strongest facts across
   sections where relevant — adjudicators skim. Refer to "the
   Beneficiary" consistently.
5. **Totality** — sustained acclaim over time (span of years, not one
   spike) + plus-factors: venue rankings, citations/h-index with field
   context, leading institutions, invited talks, government grants,
   agency interest.
6. **The event and area of ability** — restate the event/activity with
   dates; map each duty of the role to the acclaimed specialty (this
   pre-empts the ability-vs-role RFE).
7. **Closing** — consultation attached (name the signer/org), request for
   approval for the full validity period, consular notification or COS
   per the frame, signature block ("do not sign until instructed") with
   name/title/entity.

## Consultation / advisory opinion (documents/consultation.md)

Two artifacts, kept structurally distinct from recommendation letters:
1. **Request letter** to the signer (from the petitioner or beneficiary):
   what an O-1 consultation is, the field label, the role, the enclosures
   (CV + key exhibits), and the deadline.
2. **Advisory-opinion scaffold** for an individual-expert consultation
   (sciences/CS norm), for the signer to edit and sign:
   - signer's identity, credentials, and how they know the field;
   - statement that no appropriate peer group or labor organization
     exists for [field];
   - description of the Beneficiary's ability and achievements (factual,
     3-4 sourced highlights — the signer states how they learned them);
   - description of the duties to be performed;
   - whether the position requires the services of a person of
     extraordinary ability;
   - signature + contact info. (An organization may instead issue a
     "no objection" letter — file it as-is, watermark and all.)
   Conflict check before sending: the signer must not be an investor,
   advisor, or employee of the petitioner.

## Itinerary document (documents/itinerary.md)

Single employer, single site: a half-page "Explanation of the Event" —
activity description, beginning and ending dates, address. Multi-site or
agent filings: a table, one row per engagement — dates · employer legal
name + address · venue/location name + address · role/services · rate —
followed by one paragraph explaining how the engagements form one
event/activity spanning the requested validity. Every row must have a
contract exhibit behind it; no speculative rows.

## Expert letters

See `references/support-letters.md`. Draft AFTER the support letter so
each letter is assigned specific criteria to carry.

## INDEX OF EXHIBITS (documents/exhibit-index.md)

Foundational exhibits first: 1 petitioner documents (corporate/governance
or agent authorizations) · 2 contract or oral-agreement summary ·
3 itinerary/event explanation · 4 consultation letter · 5 CV — then
criterion-by-criterion in the order argued; within a criterion: expert
letters → primary evidence → contextual evidence (selectivity pages,
rankings, circulation data). Descriptions start with what the exhibit
proves ("Evidence of Completed Judging: ..."). Re-used exhibits get "See
Exhibit N", not a re-listing. Inline citations `(Exhibit N)` /
`(Exhibits N–M)` (en-dash), sentence-final; legal authorities in
footnotes only.

**Source registry** (documents/source-registry.md, printable) — build it
WHILE drafting, not after; it feeds the Stage V claim-verification log
(rfe.md) and any later RFE response. Every factual claim gets a line:
claim → exhibit number, or URL + verbatim quote + retrieval date for web
facts. LOAD-BEARING claims — what the support letter argues a criterion
from, anything about a third-party entity, anything asserting impact — get
the full row. Two tables, and the headings are a contract:
`openniw registry` parses them.

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
- **independent verifier** — who attests this OTHER than parties with a
  stake in the outcome: the beneficiary, the PETITIONER, the beneficiary's
  own company, investors. Write "NONE — self-serving" when that is the
  truth, because the officer will; then get one before filing, or cut the
  claim. This matters more here than in a self-petition: the petitioner's
  own support letter carries most of the argument, so a criterion resting
  only on it is the employer vouching for its own hire.
- **measure** — impact claims only: the number and its as-of date. Blank
  elsewhere; never manufacture precision to fill a cell.
- **gap** — what is still missing for the claim to stand ([TODO] text).

Check each new row against those already written: the same fact carrying a
different number or date is a contradiction to fix NOW, not at assembly.

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

Field label verbatim at every occurrence · "the Beneficiary" consistent ·
petitioner voice throughout (never "I, the applicant") · every entity
claim exhibit-bound · every claim has a source-registry line · every
load-bearing claim names an independent verifier or says why none exists ·
no adjective without its fact · no [TODO] left at
finalization · no dangling template instructions · criteria in regulatory
numbering · consultation distinct from recommendation letters · all
numbers match case.json · dates/validity consistent across support
letter, itinerary, contract, and I-129 worksheet.

Sources: USCIS Policy Manual Vol. 2 Part M Ch. 4, 7-8; 8 CFR 214.2(o);
letter architecture and argument patterns adapted from
juntoku9/claude_immigration_attorney (MIT); consultation practice:
deel.com advisory-opinion guide.
