# RFE Response — R1–R7 (read this whole file when a notice arrives)

Normalize once, then work: 458 of the 1,218 publicly posted APPROVED NIW cases that clearly disclose RFE status either way — out
of 4,855 posted approvals, nearly three-quarters of which say nothing either way — came through an overcome RFE (public_source
published-approval scrape, as of 2026-08). A share among posted APPROVALS, never a probability for this one.

## Standing rules (state the first three in your first reply)

1. Timeliness is **RECEIVED-BY, not postmark** — target delivery 5-7 days early (that buffer is practice, not regulation; the
   rule is receipt by the printed deadline).
2. The deadline **cannot be extended**, ever; missing it means denial as abandoned, on the record, or both (103.2(b)(13)(i)) —
   and an abandonment denial cannot be APPEALED. The only path left is a 103.5(a)(2) motion to reopen, which must show one of
   three things: the requested evidence was not material · the response WAS timely · the notice went to the wrong address (or a
   filed address change / G-28 was ignored). Attorney territory — say so.
3. **Respond ONCE, all at the same time** — a partial submission is a request for a decision on the record as-is (8 CFR
   103.2(b)(11)).
4. Eligibility is judged **as of the original filing date** (103.2(b)(12)).
5. The as-filed endeavor sentence is frozen — never reword it.
6. The response goes to the address **on the notice**, never a lockbox.

Options: complete response · partial (= decide on the record) · withdraw; advise complete — unless the plan MATERIALLY changed
since filing, which no response cures: that is withdraw-and-refile, with a licensed attorney. Price it out loud first:
withdrawal — like abandonment or denial — FORFEITS the priority date; a refiled petition takes a new one and a new fee, and 8
CFR 204.5(e) retention requires an APPROVED petition, so weigh the user's chargeability (India/China EB-2 retrogression makes it
a multi-year loss). A **NOID** is not an RFE (30 days +3 mail = 33; **+14 instead of +3** if the petitioner is abroad or an
international office issued it — the PRINTED deadline still controls; pre-denial posture, silence on a ground concedes it) and
warrants attorney review; if it cites derogatory information the petitioner did not know about, there is a right to be notified
of it and to rebut it (103.2(b)(16)(i)). A **NOIR** (post-approval intent to revoke, 8 CFR 205.2) is OUT OF SCOPE for this
workflow — different posture, no fixed regulatory period (read the notice), rebuttal on "good and sufficient cause", and only
15/18 days to appeal if revocation issues: refer to counsel immediately, and never apply the 87/33-day arithmetic to it.

## R1 Intake — two entry paths, both must work

New under `rfe/`: `letter.pdf` · `response-plan.md` · `evidence-matrix.md` · `letters-plan.md` · `supplemental-statement.md` ·
`response-letter.md` · `exhibit-index.md` · `package/`; plus `sources/petition/` for an emergency entry's filed record. Standing
rule 4: anything handed to you from elsewhere gets COPIED into the case folder first.

**Path A — prepared here**: read STATE.md, case.json, endeavor.md, documents/; copy the notice to `rfe/letter.pdf`.

**Path B — EMERGENCY ENTRY** (attorney-prepared or DIY petition, no case folder — the common case): create the folder +
STATE.md, then collect the notice (all pages) · the AS-FILED petition letter · the as-filed forms · the exhibit index · the
filed PES. Chat drops go straight into `sources/petition/`; `openniw ui intake`'s upload area writes FLAT into `sources/` and
OWNS `sources/*` for the duration — never write there while that session runs, and only after it finalizes
(done/abandoned/stale) and you delete the sentinel do you MOVE the notice and the as-filed record into `sources/petition/`,
logging the move in STATE.md. Reverse-build: the endeavor sentence extracted **VERBATIM** into `endeavor.md` as `FROZEN (as
filed) — do not reword`: for an external case the frozen text is whatever was filed, and rewording it is a material-change risk.
Then case.json + profile.md from the filed record only, every unsourced fact `[TODO]`. Say plainly what you could not
reconstruct.

**Both paths** — off the notice into STATE.md: receipt number · service center · notice (mail-out) date · the **printed
deadline** · response address · premium · RFE vs NOID · coversheet required? The printed deadline ALWAYS controls; compute only
if it is illegible — notice date + 84 + 3 mailing = **87 days** for an I-140 RFE (**+14 not +3** if the petitioner is abroad),
NOID +30+3 = **33 days**, a weekend/holiday end date rolling to the next business day; officers may shorten, never lengthen.
Milestones back from **D**: **−8wk** every fact the new letters need in hand (letters are the longest pole) · **−5wk** drafting
starts, statement done · **−3wk** first full draft · **−2wk** exhibits assembled · **−1wk** ship for delivery ≥5 days early.
Under 8 weeks: compress proportionally, name what is at risk, send letter requests DAY ONE. Then activate RFE mode in STATE.md
per SKILL.md's contract — append the `R` line AND strip the `←` from the six lines above it, or the stepper highlights the stale
marker instead of `R`.

## R2 Diagnose → rfe/response-plan.md

Quote **each challenged point in the officer's own words** (verbatim + notice page); per point the prong (or the classification,
or a whole-record finding) plus a root cause from the eight — no evidence submitted · wrong evidence type · evidence too weak ·
missing sub-element · legal misframing · factual gap · self-serving evidence only · stale/irrelevant. The root cause dictates
the fix. NIW patterns (each mirrors a prevention rule in rfe.md): credential-shaped record ("the entire record consists of
education, published work, citations, employment") · "common among researchers" (improper comparative test — say once that Prong
2 is not comparative) · authorship misread off a public Scholar profile · grant participation reduced to a share-of-output ratio
· employer claims block-quoted as unsubstantiated · foreign affiliation + "requires substantial resources" · Prong-3 flat "did
not" findings.

**Officer errors to rebut** — numbered, each paired with the corrective fact AND the exhibit that proves it (the published page
carrying the equal-contribution notation; the advisor letter naming the conceived contribution); due at D−5wk. The notice's
**"you may submit" bullets are a LITERAL checklist**: one row per bullet, answered with evidence or an explicit stated reason it
does not apply. They restate the Policy Manual's categories; most-skipped: government letters, U.S. investment "in amounts
appropriate to the relevant endeavor", non-monetary government support, evidence others use the work.

## R3 Evidence → rfe/evidence-matrix.md + a supply loop

Matrix by prong, one row per deficiency: what the officer said is missing (short quote) · what we already filed · what we must
obtain · status · date-class. **Supply loop**: ask for **ONE concrete item at a time** — "the signed [X] showing [Y], dated
before [filing date]", never "send more evidence"; as each arrives, copy it in, date-class it, update the matrix and STATE.md,
ask the next.

Where the officer calls something UNSUBSTANTIATED, read the claim's independent-verifier cell in `documents/source-registry.md`
(drafting.md) before deciding what to obtain — Path B builds those cells while reverse-reading the filed record. If it says NONE,
the item to obtain is an INDEPENDENT attestation, not another document from the same interested party; sending more of what the
officer already discounted is the commonest way a response fails.

**At-time-of-filing doctrine**: eligibility is judged as of the filing date, but documents CREATED later that prove facts in
place at filing are fine (new letters about old work, citation records of pre-filing papers). Date-class every item: pre-filing
(the target) · post-filing as continuation of a NAMED pre-filing thread · not worth it. Tag post-filing items `[post-filing]`
and name the anchor: original PES project number, start date, collaborator. Present growth as before→after pairs on the priority
date, making post-filing data evidence OF the at-filing trajectory.

**Government / quasi-government letters — ask EVERY user**, even when nothing in the record suggests it ("any connection to a
government or quasi-government agency that could sign a letter?"): the class practitioners describe as the only one able to
support all three prongs (an attorney-practice observation, not a USCIS rule). Signers: a representative of an agency that
FUNDED the applicant's project · a researcher at a national lab they collaborate(d) with · any direct government collaborator.
Topics: agency expertise in the area → the endeavor's national importance (P1) · knows the applicant or work personally →
achievements and how they position the applicant to continue (P2) · agency interested in HIRING → says so, and that the U.S.
benefits even if other U.S. workers are available (P3).

**Citation-example refresh** (scoring rules: evidence.md): 8-10 NEW independent examples, DIFFERENT from those used in the
original filing (reuse only if no additional strong ones exist); **several per each most-cited paper**; published original
research preferred; nothing accepted-but-unpublished. `openniw harvest` → your scoring pass → `citations/scored.json` → `openniw
ui citations` to pick → `openniw highlight <pdf> --needle X`, highlighting ONLY the in-text citations and the reference-list
entry. Write both pre-emptions into the response: the work is **singled out** (its use differs from the citing author's other
citations), and the citing authors **collectively represent the field**, not "a handful of peers" (spread across subfields,
institution types, countries, venues). Never emphasize citer prestige.

## R4 Letters → rfe/letters-plan.md

One row per letter: signer + credential · the SPECIFIC challenged finding it rebuts (quote it) · unique angle, no two letters
covering the same ground · dependent/independent · status. New letters help but are not required; proceed without a recommender
who cannot confirm in time. Structures and signing: `support-letters.md`. Targets: 2-3 **independent** recommenders who cited
the work and can discuss ≥1-2 OTHER notable citations by third parties, taken from R3's selected citing authors · plus
**dependent** letters (first-hand → P1+P2; a U.S.-based dependent may also state that the waiver serves the national interest).
Keep two classes separate: expert recommendation letters ≠ **testimonial letters**, factual attestations from interested parties
(employer/CEO, investor, customer), expressly "not offered as an expert reference"; the employer testimonial names its
corroborating exhibits inline. Counts quoted in a letter carry an as-of month, with the Scholar exhibit re-captured at signing.
Request day one, finalize last.

## R5 Statement → rfe/supplemental-statement.md

First person, "To: USCIS", drafts circulating undated and unsigned. Six parts — §1-§5 plus a mandatory **List of References**
keyed to in-text numbers, covering publications (including the applicant's own), documents, government and media sources and
URLs, weighted toward U.S. government sources.

1. **Proposed Endeavor** — restate it EXACTLY as filed; any deviation may read as a material change and support a denial. Only
   AFTER the verbatim restatement may you expand, then the firewall sentence ("… clarifies and provides additional evidence; it
   does not replace or materially alter the endeavor described in the petition."), one unified theme with N reinforcing pillars,
   and — if employed — the employer as deployment pathway.
2. **Future Research Plans** — an overview paragraph, then **2-3 specific projects each carrying technical detail** (experiments
   planned, models to be developed), removing ambiguity about the work; note existing or expected funding; end each with why it
   benefits the U.S., ideally on U.S. government data. Build it from a progress-mapping table: one row per topic AS ENUMERATED
   IN THE ORIGINAL PES → outputs since, each project naming the original topic number and its start month. A topic the record no
   longer supports is NOT dropped: keep its subject, timeline and collaborator, shift the center of gravity to what is
   defensible.
3. **Broader Implications** — the X→Y→Z impact chain; the one place assertion without an exhibit is sanctioned — state the
   significance clearly. Optional job-creation claim via an employer letter. Dissemination plan.
4. **Past Accomplishments and Interest** — education, skills, record of success (awards as ratios, funding helped secure, media,
   patents, contracts), progress made, INBOUND interest (peer inquiries, invitations).
5. **Plans for Future Employment in the U.S.** — no job offer is required, but employment feeds the well-positioned and
   national-importance findings. *Branch A, employed in the U.S.*: job and research duties, characterizing **≥50% of the work as
   research**, and how the role enables the endeavor. *Branch B (student / visiting scholar / unemployed / abroad)*:
   research-oriented offers or hiring interest; if none, start looking and obtain a **letter of intent** from a prospective
   employer or the advisor. **Industry warning**: USCIS heavily scrutinizes industry applicants and challenges that the endeavor
   benefits only the employer — answer affirmatively with documented national distribution plus a dissemination paragraph
   (publications, patents as public disclosure, open source, peer review). Labor-certification impracticality FACTS (founder,
   equity share, a role built around the applicant's own research rather than a pre-existing vacancy) go here as facts; the
   legal argument stays in the response letter.

## R6 Assemble → rfe/response-letter.md, exhibit-index.md, package/

The response letter **mirrors the notice's own order and headings**, and every point **leads with new evidence** — "Enclosed as
New Exhibit X, …" — then argues: the officer read the record and was not persuaded, and re-argument alone is what denials quote
back. Answer every "you may submit" bullet, including the inapplicable ones. The exhibit index **QUOTES the RFE sentence each
exhibit answers**, writes down WHY it is evidence — never leave the inferential step to the officer — tags date-class, and ends
with open questions.

`rfe/package/` mirrors the response's sections: `1_evidence/` (Part A academic, Part B company) · `2_citations/`
(all_citing_papers → candidate + rejection log → selected → submitted) · `3_recognition/` (awards with third-party corroboration
of the ratio · peer-review invitation/acceptance/completion trails · media, each foreign item as original + certified
translation) · `4_personal_statement/` · `5_testimonial_letters/` · `6_rec_letters/`.

**Pre-ship red team**: before anything is printed, run `rfe.md`'s twelve prevention rules AND the claim-verification log over
the assembled package — each officer finding maps back to a rule unsatisfied at filing — and re-check every count against
case.json; numbers drift between filing and RFE.

**Physical order**: the premium coversheet (if the notice includes one) and then the ORIGINAL notice sit on top of everything —
submitting without them delays processing and may cause a denial. Then response letter → supplemental statement → letters →
exhibits in index order; mail and translation rules as in forms.md. **Where**: the address on the notice, never a lockbox. Paper
is default; upload online ONLY if the user's myUSCIS account actually shows this RFE with a respond option (then received = the
e-filing timestamp). **Premium**: an RFE stops the clock, and a **fresh full 45-business-day** NIW window starts when USCIS
receives the response (8 CFR 106.4(f)(3)); not on premium, an I-907 upgrade is the only lever — $2,965 as of 2026-03-01
(re-verify G-1055), on its OWN payment form (forms.md), and settle its CHANNEL before anything is mailed: enclosed WITH the
paper response it rides along to the notice address, but a STANDALONE upgrade goes to the uscis.gov/i-907 direct-filing chart
address, which is NOT the response address on the notice. Sources conflict as of 2026-08 on whether a pending IOE-receipted
I-140 can add premium online (forms.md says yes; USCIS "Forms Available to File Online", 07/24/2026, says I-907 for an I-140 is
paper-only) — verify both, default to paper. On regular processing the wait is unbounded — promise no timeline. **Delivery**,
back from the received-by date: courier with tracking and signature · delivery 5-7 days early (practice, not rule) · a complete
copy kept in the case folder · tracking and delivery confirmation logged in STATE.md.

**If the decision is a denial**: the I-290B clock is **30 days from the decision date** (33 if the decision was mailed; 15/18 to
appeal a revocation), cannot be extended, and runs while the user is still hunting for counsel: compute that date, say it out
loud, and tell them to engage an attorney NOW. I-290B is $800, paper-only, no premium; motion to reopen vs motion to reconsider
vs AAO appeal vs refile is attorney territory.

## R7 Contribute (OPTIONAL — always ask, never assume)

After the response ships, or when the decision arrives, offer ONCE an anonymous data point + suggestions; if declined, drop it.
Fields (GitHub issue-form ids — the contract): `category` · `field` · `citations` · `publications` · `filing_month` (YYYY-MM) ·
`premium` · `rfe` · `outcome` · `processing_days` · `suggestion` · `consent`. The form REQUIRES category, field, citations,
filing_month, rfe, outcome — plus `consent`, an anonymization checkbox only the user can tick: on the URL path tell them to tick
it before submitting, and on the `gh` path put an equivalent confirmation line in the body. Dropdown values must match the
form's option text exactly — a prefill value that does not match is silently DROPPED — category `NIW|EB1A|EB1B|O1|Other` (always
`NIW` here); rfe `No RFE | RFE received — overcame (approved) | RFE received — denied | NOID received | Prefer not to say`;
outcome `Approved|Denied|Withdrawn|Still pending`; premium `No | Premium from filing | Upgraded mid-case | Prefer not to say`;
`field` is one of the form's own 16 discipline buckets (last: `Other fields`) — if that list is not in front of you, leave
`field` OUT of the URL rather than guess and let the user pick it.

**Anonymization is absolute**: no name, email, receipt or case number, employer, recommender names, or identifying institution.
Compose the values, SHOW them to the user, get explicit approval before sending, and never include case identifiers even if
offered. Submit, in order: (1) `gh` present and authenticated (`gh auth status`) → `gh issue create --repo HHHHHejia/openniw
--title "[data] case outcome" --label data-point --body <approved body, one "Label: value" line per field, ending with the
anonymization confirmation>` — if it fails because the `data-point` label does not exist in the repo yet, retry once WITHOUT
`--label`; (2) otherwise open the prefilled form URL
`https://github.com/HHHHHejia/openniw/issues/new?template=data-point.yml&category=NIW&…` (URL-encode values) so the user signs
in, ticks the anonymization box and submits it; (3) else print the ready-to-paste body.

Sources: 8 CFR 103.2(a)(7), (b)(8), (b)(11)–(b)(16), 103.5, 106.4, 204.5(e), 205.2 (eCFR) · USCIS Policy Manual Vol. 1 Pt. E Ch.
6 §F (84+3/87, 30+3/33, +14 abroad, received-by) and Vol. 6 Pt. F Ch. 5 (NIW, Jan 2025 update) · uscis.gov premium, i-290b
(06/01/2026) and file-online pages · G-1055 (ed. 05/29/26); verified 2026-08-03 — re-verify fees and addresses before filing.
Overcome-RFE share from the public_source published-approval scrape (2026-08). Response architecture, government-letters doctrine
and statement template distilled from a de-identified real NIW RFE cycle; control-file patterns adapted from
juntoku9/claude_immigration_attorney (MIT).
