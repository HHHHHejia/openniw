# RFE mode — the R1–R7 response workflow (O-1)

**The response is the PETITIONER's filing.** The beneficiary is not an "affected party" (8 CFR 103.3(a)(1)(iii)(B)) and signs
nothing USCIS treats as the response: you draft; the petitioner's signatory — whoever signed the I-129, or the attorney of record on
a G-28 — signs and files. Say once and plainly that a licensed immigration attorney's review is worth considering, and more firmly
for a **NOID**: a pre-denial notice stating USCIS's own affirmative theory, so every stated ground must be rebutted head-on and
silence on a ground concedes it.

**Four rules that never bend** (8 CFR 103.2, verified 2026-08-03). Timeliness is **received-by, not postmark** (103.2(a)(7)(i));
target delivery 5-7 days early. The deadline **cannot be extended, ever** (103.2(b)(8)(iv)). **Respond ONCE, everything at once**,
original notice on top — a partial submission is adjudicated as a request for a decision on the record (103.2(b)(11)). **Eligibility
is judged as of the FILING date** (103.2(b)(1), (b)(12)): new DOCUMENTS proving pre-filing facts are fine, new ACHIEVEMENTS cannot
create eligibility. Miss the deadline and the petition is denied as abandoned, on the record, or both (103.2(b)(13)(i)); an
abandonment denial cannot be appealed, and the only recovery is a motion to reopen (103.5(a)(2)) on three grounds — the evidence was
not material, the response was in fact timely, or the notice went to the wrong address.

Normalize, never forecast: of 128 posted APPROVED O-1 cases (evaluation.md's 123-case benchmark pool plus 5 lacking citation data),
29 disclosed their RFE status — 21 came through an overcome RFE, 8 reported none. One firm's self-published approvals, no denials in
the pool, 77% of posts silent: anecdote-grade, never a rate, never this case's odds.

## R1 Intake

Announce RFE mode, append the seventh stage line + RFE block to STATE.md (template in SKILL.md), and put the notice into the case
folder as `rfe/letter.pdf` — both paths need it there. **Path A — prepared with this skill**: everything else is on disk.

**Path B — EMERGENCY ENTRY** (attorney-prepared or DIY petition, no case folder — the common case). Create `o1-case/` + STATE.md and
collect the AS-FILED record: petition letter, I-129 + O/P supplement, consultation, contracts, itinerary, exhibit index. Chat drops
go straight into `sources/petition/` (standing rule 4); browser uploads via `openniw ui intake` land FLAT in `sources/`, which the
server owns while the session runs — never write there, and only once it finalizes (done/abandoned/stale) and you delete the
sentinel do you MOVE those files into `sources/petition/`, logging the move in STATE.md. Then REVERSE-BUILD, extracting **VERBATIM**
the petitioner legal name + structure, field label, role + duties, event dates and itinerary rows. The frozen frame is whatever was
filed — NEVER reword it: a pending petition is adjudicated on the record as filed (103.2(b)(1), (b)(12)), and rewording reads as a
different petition (post-approval the same change needs an amended petition, 214.2(o)(2)(iv)(D)). Save petition-frame.md `FROZEN (as
filed <date>)`, build case.json + profile.md from the filed record with every unsourceable fact `[TODO]`, then name WHICH frozen
items the notice attacks.

**Both paths — off the notice into STATE.md**: receipt number · FILING date (the eligibility date) · service center · premium yes/no
· signatory and attorney of record · **the response address printed on the notice** · **whether the notice carries a
premium/response coversheet** · RFE vs NOID · notice DATE (mail-out) · the **PRINTED deadline**, which always beats a computed one.
If computing: I-129 RFE = notice + 84 + 3 = **87 days**; NOID = +30 + 3 = **33 days**; a weekend/holiday end date rolls to the next
business day. The mail allowance keys to the party the notice was MAILED to — for an O-1 the U.S. petitioner or attorney of record
(a foreign employer must petition through a U.S. agent, 214.2(o)(2)(i)), so **+3**; +14 applies only where USCIS mailed abroad or an
international office issued it, rare for an I-129 O. Officers may shorten, never lengthen. Work back in weeks: −1 sign and ship · −2
exhibits and index · −3 first draft · −4 documents in hand · −6 every consultation and letter request OUT (the long pole); week 1 is
R2. A 33-day NOID compresses this to days.

**Status runway — raise it unprompted.** O-1 has no cap-gap; a pending COS is authorized stay but gives NO work authorization until
approval, and a COS denied after the I-94 expired starts unlawful presence the next day. Travel while a COS pends is generally
treated as abandoning it (practitioner guidance, unconfirmed against a primary text). Compute the runway against deadline +
adjudication time; the levers are premium and the consular pivot, and R2's withdraw branch turns on this number.

## R2 Diagnose → `rfe/response-plan.md`

Real O-1A RFEs still track USCIS's own O-1A template — a 2013 draft for comment, never finalized, still the observed skeleton —
section by section, each branching "you did not submit evidence" vs. "the evidence is insufficient". Use it as a map, but always
diagnose from the officer's actual words. One row per challenged point: (1) **the officer's own words**, quoted exactly; (2)
**class** — formal gap (contract · event+itinerary · consultation · translations: the mandatory initial evidence of 214.2(o)(2)(ii),
independent of the criteria and the cheapest complete cures, so fix these first) · structure · criterion substance · totality ·
comparable evidence; (3) **the sub-element attacked**, not the criterion (critical role = role critical AND organization
distinguished — officers concede one prong and deny the other); (4) **root cause**, one of 8 — no evidence · wrong type · too weak ·
missing sub-element · legal misframing · factual gap · self-serving only · stale; (5) **fixability** Yes / Partially / Unlikely.

**Officer errors to rebut**, each paired with the corrective fact AND the exhibit that proves it: citing *Kazarian* or other
I-140/EB-1A case law as the governing standard — O-1 DOES apply a second-step totality determination, but it comes from Policy
Manual Vol. 2 Pt. M Ch. 4 (and the 1994 preamble), not EB-1A final-merits case law, so argue the totality is satisfied ON THIS
RECORD and never that no totality review exists · ignoring prospective remuneration under criterion 8 or comparable evidence ·
reading the field label narrowly against Ch. 4.F's "related occupations sharing skillsets". Treat the notice's "you may submit"
bullets as a **LITERAL checklist**: each gets evidence or a stated reason it does not apply.

**Triage.** Only 3 criteria are needed, so explicitly withdrawing a weak one ("The Petitioner respectfully withdraws the claim
under…") and reinforcing three strong ones beats defending five. **Withdraw-and-refile** belongs on the table when a gap is
unwinnable under 103.2(b)(12), the petitioner posture is structurally wrong, or the window is too short for decisive evidence;
refiling with a new fee is permitted, but the prior filing's facts "shall otherwise be material" to it (103.2(b)(15)), so a refile
must FIX the weakness. **Gate that branch on R1's status runway before recommending it**: state (a) whether the beneficiary is
inside the U.S. on a pending COS; (b) that withdrawing the I-129 ends that pending COS and, if the I-94 has already expired,
unlawful presence accrues from that point (180+ days → a 3-year bar); (c) the consular-notification pivot as the alternative; (d)
that this branch specifically warrants licensed-attorney review before the petitioner decides. If the beneficiary is abroad or in
independent status, say so and proceed. Present it as a ranked recommendation with fee, timing AND status cost; the PETITIONER
decides, here and on every strategic call, before R3 starts.

## R3 Evidence → `rfe/evidence-matrix.md` + the supply loop

One row per deficiency in the notice's own order — deficiency-driven, not criterion-driven. Columns: **quoted deficiency ·
sub-element · what the officer says is missing · what the record already has (Exhibit N) · what we must obtain · who produces it ·
status · fact-as-of date**. Where the officer calls a claim unsupported or notes it rests on the petitioner's own say-so, read
that claim's independent-verifier cell in `documents/source-registry.md` (drafting.md) before deciding what to obtain: if it says
NONE, the item to obtain is an INDEPENDENT attestation, not another document from the petitioner or the beneficiary's own company.
**Date-class every item** against the filing date: `pre-filing` · `post-filing, continuation of <named
pre-filing thread>` · `not worth it`. Documents CREATED after filing that prove facts in place AT filing are fine (a citation report
on pre-filing papers, a letter memorializing a pre-filing relationship, a replacement consultation); post-filing achievements appear
only as labeled corroboration. **Supply loop — ask for ONE concrete item at a time**: never "send more evidence", but "the signed
authorization letter from [Employer], dated before [filing date], stating that [Agent] may file on its behalf". As each arrives,
copy it into `evidence/exhibits/`, date-class it, update the matrix and STATE.md, then ask the next. The petitioner produces or
certifies every corporate exhibit.

**Cures.** Criterion menus and the mandatory documentary layer are in `references/evidence.md`, petitioner-structure packages in
`references/petition-frame.md` — collect from there. The RFE-stage deltas: cure the SUB-ELEMENT the officer hit, not the criterion;
every authorization, contract and governance document must PREDATE filing (ability to pay is not an O-1 requirement); the itinerary
table must match 214.2(o)(2)(iv)(E)(2) field-for-field with the contract or LOA behind EVERY row and speculative rows deleted — if
full multi-employer agency can't be proven, a validity limited to the petitioner's own engagements beats denial; for an
ability-vs-role attack add a duty-by-duty map to the frozen field label under Ch. 4.F's broad reading. Where criterion 5 or 6 was
attacked, rerun evidence.md's citation pipeline and frame the examples as the influence of PRE-filing work, never as a new
achievement. And the one cure the notice itself invites:
- **A NEW consultation mid-RFE**, content per 8 CFR 214.2(o)(5)(ii)(A): ability + achievements, nature of the duties, whether the
  position requires a person of extraordinary ability, and supporting facts, signed by an authorized official on letterhead (a
  letter of no objection is accepted in lieu); the signer must be independent — never an investor, advisor, employee, or
  recommendation-letter writer. Turnaround figures ("days to two weeks and free" for an individual expert, "a fee and weeks" for a
  listed peer group) are practitioner-reported — verify with the signer, never quote them. No peer group? Document the absence or
  failed attempt and ask USCIS to decide on the record ((o)(5)(i)(G)); a non-labor-org opinion where a union covers the occupation
  adds a 15-day forwarding cycle ((o)(5)(i)(F)).

## R4 Letters → `rfe/letters-plan.md`

One row per letter: **signer + credential · the SPECIFIC challenged finding it rebuts, quoted · unique angle · dependent or
independent · status**. A letter that praises without touching a cited deficiency adds nothing. Three classes, kept separate
(structures in `references/support-letters.md`): the **replacement consultation**, whose signer writes nothing else in the package ·
**independent expert letters** keyed to the attacked sub-elements, analyzing specific results rather than the person · **factual
testimonials** (employer, investor, customer) — first-hand fact, not evaluation. Request week 1, finalize last.

## R5 Statement → `rfe/supplemental-letter.md`

In the PETITIONER's voice, for the petitioner's signatory — an O-1 has no self-petitioner personal statement. Sections: (1) the
frozen frame restated VERBATIM plus a firewall sentence — "This supplemental letter clarifies the record as filed; it does not
replace or materially alter the petition, the offered position, or its terms."; (2) the petitioner facts the notice questioned, each
exhibit-bound; (3) employment terms exactly as filed; (4) governance or agent authority where attacked; (5) the duty-by-duty map of
role to field label; (6) the request plus any criterion withdrawal. Where the notice challenges facts only the beneficiary can
attest to, add a short signed beneficiary declaration as an EXHIBIT — supporting evidence, never the response itself.

## R6 Assemble → `rfe/response-letter.md`, `rfe/exhibit-index.md`, `rfe/package/`

**Response letter** MIRRORS the notice's own order and headings, one section per challenged point: quote the officer's finding →
state the correct standard with its citation (8 CFR 214.2(o) + Policy Manual Vol. 2 Pt. M, never *Kazarian*) → **lead with NEW
evidence** ("Enclosed as New Exhibit R-3 …") → tie back to the original exhibits → close the sub-element attacked. The officer
already read the original record and was not persuaded; re-argument alone is what denials quote back. Tone: "We respectfully
submit", petitioner letterhead, authorized signatory. Add a **cross-walk page** (RFE issue ↔ resolving exhibit(s) ↔ what it proves)
and an **exhibit index** numbering new exhibits `New Exhibit R-1…` after the original series, each entry QUOTING the RFE sentence it
answers.

**Package order**: the premium/response coversheet if the notice includes one → the **ORIGINAL** RFE/NOID notice → signed response
letter → cross-walk → exhibit index → new exhibits in index order → signed I-907 + separate check if filed. Premium notices ship
with that coversheet and warn that "submission of evidence without the coversheet and this letter will delay processing and may
result in a denial" — quote it. Assembly, translation and mail rules per `references/forms.md`; `openniw docx <md>` converts drafts
for signature.

**Where and how.** Send to the address printed ON THE NOTICE — the service center working the case, never a lockbox — and read it
before booking a carrier: a street address takes a courier with tracking and "Direct Signature Required"; a P.O. Box cannot receive
FedEx or UPS at all, so use USPS Priority Mail Express with tracking. O-1 I-129 is not online-filable, so paper is the default;
offer online upload ONLY if the myUSCIS account actually shows this RFE with a respond/upload option — an online response counts as
received on its e-filing TIMESTAMP, weekends and holidays included, while paper must be physically DELIVERED by the printed date.

**Premium.** The clock STOPS and a fresh full 15 business days starts when USCIS RECEIVES the response (8 CFR 106.4(f)(3)), so an
early complete response is decided sooner and a non-premium case may file I-907 to force that window ($2,965 postmarked on/after
2026-03-01 — verify at uscis.gov/g-1055). Channel: an I-907 enclosed WITH the paper response rides along to the notice address; a
STANDALONE I-907 upgrade on a pending IOE-receipted O petition may be filable online, and otherwise follows the uscis.gov/i-907
direct-filing chart, not the notice address — check both ("Forms Available to File Online" and that chart) first, because sources
conflict as of 2026-08. Without premium the wait is unbounded. Before it ships, re-run rfe.md's twelve prevention rules and
re-verify every number against case.json.

**Petitioner hand-off kit** (mirrors Stage V's handoff.md): what they receive, what they sign, and what they verify against their
own records (entity facts, wage, dates, itinerary) · the exact address off the notice and the carrier that can reach it · a delivery
checklist counting back from the received-by target · a COMPLETE copy of everything shipped, kept in `rfe/package/` as the record
for any later refile or motion, with tracking number and delivery confirmation logged in STATE.md's Decision log · what happens next
(if denied, I-290B within 30/33 days, $800; practitioner consensus, not a rule: a corrected refile with premium beats an AAO appeal,
except where the denial is legally wrong on an otherwise good record or a filing-date/status equity must be preserved).

## R7 Contribute (OPTIONAL — always ask, never assume)

After the response ships, or when the decision arrives, offer ONCE: an anonymous data point plus improvement suggestions; if
declined, drop it. Fields (GitHub issue-form field ids — the contract): `category` · `field` · `citations` · `publications` ·
`filing_month` (YYYY-MM) · `premium` · `rfe` · `outcome` · `processing_days` · `suggestion`. Dropdown values must match the form's
option text EXACTLY or GitHub silently drops them — `category` O1 · `premium` `No | Premium from filing | Upgraded mid-case | Prefer
not to say` · `rfe` `No RFE | RFE received — overcame (approved) | RFE received — denied | NOID received | Prefer not to say` ·
`outcome` `Approved | Denied | Withdrawn | Still pending` · `field` from the form's own 16-item list (e.g. "Computer Science & AI",
not "Computer Science").

**Anonymization is absolute**: no name, email, receipt or case number, employer, petitioner entity, recommender names, or
identifying institution. Compose the values from case.json, SHOW them in full, get explicit approval, never include case identifiers
even if offered. Submit in order: (1) `gh` present and authenticated (`gh auth status`) → `gh issue create --repo HHHHHejia/openniw
--title "[data] case outcome" --label data-point --body <approved body>`; (2) else open the prefilled form URL
`https://github.com/HHHHHejia/openniw/issues/new?template=data-point.yml&category=<v>&field=<v>&…` (all field ids, URL-encoded) for
the user to submit under their own login; (3) else print the ready-to-paste body and the plain form URL. Never submit without an
explicit go-ahead.

Sources (verified 2026-08-03): 8 CFR 103.2, 103.3, 103.5, 106.4, 214.2(o) via eCFR (point-in-time 2026-07-30); Policy Manual Vol. 1
Pt. E Ch. 6 § F (84/87, 30/33, received-by) and Vol. 2 Pt. M Ch. 3, 4, 7; the O-1A RFE template — 2013 draft for comment, never
finalized — at uscis.gov/sites/default/files/document/legal-docs/O-1A-SEBA.pdf; premium fee "Adjustment to Premium Processing Fees",
FR doc 2026-00321 (Jan 12, 2026), eff. 2026-03-01, verified at uscis.gov/g-1055. Response discipline adapted from
juntoku9/claude_immigration_attorney (MIT); RFE patterns, consultation turnarounds and the refile-vs-appeal heuristic are
practitioner-reported (arvian-immigration.com, greencardlink.com, immi-usa.com, tukki.ai).
