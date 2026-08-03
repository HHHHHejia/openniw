# RFE / NOID response — stages R1–R7 (read when a notice arrives)

Prevention stays in `rfe.md`; this is the executable response workflow, replacing the numbered
stages for the duration (II·b–IV mechanics get reused), for a case prepared here or one an
attorney filed years ago; standing rule 4 covers every file the user hands over. Normalize once:
304 of the 577 publicly posted APPROVED EB-1A cases that disclose RFE status (out of 2,386 posted
approvals — three-quarters say nothing either way) came through an overcome RFE — a share among
posted APPROVALS, never a probability that this one is overcome. Case-folder
additions — `rfe/`: letter.pdf (the notice) · response-plan · evidence-matrix · letters-plan ·
supplemental-statement · response-letter · exhibit-index (all .md) · package/; plus
`sources/petition/` for an emergency entry's filed record. STATE.md takes two additions when RFE
mode activates: a seventh line APPENDED to the stage checklist, and a block below it. The six keep
their exact format but LOSE the `←` marker (finished stages `[x]`; on an emergency entry the six
stay unchecked and unmarked) — the stepper calls the FIRST `←`-bearing line current, so a stale
marker above `R` steals the highlight. Companions predating the R stage ignore the line, showing six.

```
- [ ] R    RFE        ← in progress

## RFE response (received: YYYY-MM-DD · notice date: YYYY-MM-DD · DEADLINE: YYYY-MM-DD)
- [ ] R1 Intake
- [ ] R2 Diagnose
- [ ] R3 Evidence
- [ ] R4 Letters
- [ ] R5 Statement
- [ ] R6 Assemble
- [ ] R7 Contribute (optional)
```

## R1 Intake — the clock first, then the record
**The clock, before any reconstruction.** Read off the notice into STATE.md: mail-out DATE, printed
response DEADLINE, response ADDRESS, receipt number, RFE or NOID, and whether a premium COVERSHEET
is enclosed; ask whether the case is in premium; copy the notice (all pages) to `rfe/letter.pdf` —
the original leaves with the package.
- **Three legal options exist** (8 CFR 103.2(b)(11)): a complete response · a partial response,
  which is an irrevocable request for a decision on the record · WITHDRAW the petition. Advise a
  complete response — unless the work or the field genuinely changed AFTER filing, which no
  response cures (eligibility is judged as of the filing date and the frozen field definition may
  never be reworded): that is withdraw-and-refile territory, with a licensed attorney.
- The printed deadline ALWAYS controls; never substitute a computed default. Defaults only if none
  is printed (8 CFR 103.2(b)(8)(iv); PM Vol. 1 Pt. E Ch. 6, as of 2026-08): I-140 RFE = notice
  date + 84 + 3 mail = **87 days**; NOID = +30 +3 = **33 days**; +14 instead of +3 if the
  petitioner resides abroad or an international field office issued the notice; a weekend/holiday
  end date rolls to the next business day. Officers may shorten the window, never lengthen it.
- Timeliness is **RECEIVED-BY, not postmark** — target delivery 5–7 days early. The deadline
  **cannot be extended**; no grace period exists. Respond **ONCE**: everything ships together, with
  the original notice on top.
- Plan backwards: letters requested day 1 (signatures are the long pole — weeks), evidence +
  drafting weeks 2–6, exhibits −2wk, delivery −1wk. **Under 8 weeks left**: compress
  proportionally, name out loud which items are at risk, send every letter request on DAY ONE, and
  say plainly whether the strongest available package can be assembled before the received-by date.
- A **NOID** = a preliminary decision to deny: rebut every stated ground head-on (silence concedes)
  by the DEADLINE PRINTED ON THE NOTICE — 30 days + 3 mail (33; +14 abroad) is the ceiling, never
  more; if it cites derogatory information the petitioner did not know about, there is a right to
  rebut it (103.2(b)(16)(i)). Recommend counsel. A **NOIR** (post-approval intent to revoke) is out
  of scope for this workflow — different posture, no fixed regulatory period, and only 15/18 days
  to appeal if revocation issues: refer to counsel immediately.

**Then establish the record. Path A** (case prepared here): read STATE.md, case.json,
claim-frame.md and the filed documents. **Path B — EMERGENCY ENTRY** (attorney-prepared or DIY
petition, no case folder — the common case): create the folder + STATE.md, then ask for, in order,
the RFE/NOID notice · the AS-FILED petition letter · the as-filed I-140 · the exhibit index — chat
drop or `openniw ui intake` (its upload area owns `sources/`) — the petition materials stored in
`sources/petition/`. Then REVERSE-BUILD the case file: extract VERBATIM from the as-filed letter
the **field-of-endeavor definition** and the **claimed-criteria list**. Whatever was filed IS the
frozen frame; never improve or reword it — a shifted field definition mid-RFE is a material-change
risk. Build case.json + profile.md from the filed record (venues, years, authorship positions,
counts + as-of dates, exhibit numbers); anything unsourceable becomes `[TODO]`, never a guess, and
you say plainly what could not be reconstructed. Mark claim-frame.md "FROZEN AT FILING (as filed)".

## R2 Diagnose → `rfe/response-plan.md`
**Field check first.** The notice's intro names the field USCIS is adjudicating; if it differs
from the frozen definition, correct it with objective taxonomy (venue categories, society
sections, grant panels) and name the comparison population — never adopt a new field definition.
**Quote every finding in the officer's own words**, one row each, in the notice's order, and
classify it; step 1 and step 2 need different answers. *Step 1* = a criterion's plain element
unproven ("Award(s) Appear to be Local or Regional"; associations do not "Require Outstanding
Achievements"; contributions "not of Major Significance") — answerable with DOCUMENTS;
sub-elements and proof types live in `evidence.md`. *Step 2 / final merits* = not "sustained"
acclaim, not "one of that small percentage… at the very top" — answerable only by a rebuilt
narrative plus benchmarking evidence; more criterion exhibits do not move it, and this is where
petitions die (R5, R6). Flag separately: translations · (h)(5) intent · prospective benefit ·
comparable evidence. **Root-cause each finding** (pick one): no evidence submitted · wrong
evidence type · evidence too weak · missing sub-element · legal misframing · factual gap ·
self-serving evidence only · stale/irrelevant. Cause dictates fix, and substitution beats addition
— produce the national award, don't argue the regional one. **Triage each challenged criterion —
Fixable? Yes / Partially / Unlikely.** Unlikely + ≥3 other criteria solid → withdraw the CRITERION
CLAIM (never the petition — that is R1's third option) explicitly: "the Petitioner respectfully
withdraws the claim under 8 CFR 204.5(h)(3)(…) and relies on the following three criteria" — only
3 of 10 are needed and a doomed claim drags the rest down.
Unlikely + exactly 3 claimed → fix it, or ADD a criterion never argued initially — allowed in an
RFE response if every supporting fact predates filing (never on appeal). Partially → substitute
evidence, don't re-argue the same exhibits. Never leave a finding unaddressed, and treat the
notice's **"you may submit" bullets as a literal checklist**: each gets evidence or a stated
reason it does not apply. **Officer errors to rebut** — each paired with the corrective fact AND
the exhibit that proves it. Where the notice demands what the regulation does not require (a
citation minimum at step 1): Policy Manual 6F2 — an officer "may not limit the kind of evidence"
and must "articulate the specific reasons"; *Kazarian*, 596 F.3d 1115, 1124–25, and *Love Korean
Church*, 549 F.3d 749, 758 — no requirements "beyond those set forth at 8 CFR 204.5". Say it
respectfully, then satisfy the demand anyway. Do NOT build on *Mukherji v. Miller* (D. Neb. 2026)
— the AAO still applies the two-step framework; that fight belongs in federal court, with counsel.
Pre-flight the plan against rfe.md's twelve prevention rules.

## R3 Evidence → `rfe/evidence-matrix.md` + the supply loop
Matrix, one row per challenged criterion × deficiency plus a step-2 row: finding | what the
officer said is missing | what we filed (exhibit #) | what we must obtain | status | date-class.
**The supply loop** is the heart of this stage: ask for ONE concrete item at a time, named exactly
("the signed editor letter confirming the 7 reviews you completed 2021–2023"), never a vague "send
more evidence"; as each arrives, copy it into `evidence/exhibits/`, date-class it, update the
matrix and STATE.md, then ask for the next. **Date-class everything**: eligibility is judged AS OF
the filing date (8 CFR 103.2(b)(12); *Katigbak*, 14 I&N Dec. 45). *Pre-filing* (the default)
proves a fact that existed at filing. *Post-filing as continuation of <named pre-filing thread>*
is a document CREATED after filing evidencing pre-filing facts (a letter written now about 2022
work, a citation report regenerated today for pre-filing papers) — always framed as the continuing
impact OF the pre-filing work, not a new achievement. *Not worth it* = something that OCCURRED
after filing (new award, paper, role): it cannot establish eligibility and must never fix a
deficient criterion. **Citation refresh** feeds criteria (v)/(vi) and answers the
aggregate-citations failure: `openniw harvest` → your scoring pass (independence, full-text
verification, depth 1–9, negative quarantine — `evidence.md`) → `citations/scored.json` → `openniw
ui citations` → `openniw highlight <pdf> --needle "<surname>"`. Deliver PER-CONTRIBUTION splits:
each contribution with its own citation count, citing institutions and quotes.

## R4 Letters → `rfe/letters-plan.md`
One row per new letter: signer + credential · the SPECIFIC challenged finding it rebuts (quoted) ·
unique angle · independent/dependent · status. New independent letters are the highest-yield RFE
evidence: prefer an expert USCIS has not seen, who knows the work from the published record. No
two cover the same ground; each names what other groups DID differently because of the pre-filing
work, with dates and numbers, attesting to facts as of the filing date (bar and skeleton:
`support-letters.md`). Factual testimonials (employer, investor, customer, editor) are
attestations from interested parties, NOT expert opinions — keep the two classes separate.

## R5 Statement → `rfe/supplemental-statement.md`
One signed, first-person document doing two jobs — the E11 template invites "a statement from the
beneficiary detailing plans on how they intend to continue work in the United States", and (h)(5)
intent is RFE'd even when every criterion is met. (1) **Intent to continue work** (structure:
`drafting.md`): the FROZEN field definition restated VERBATIM, then current projects and position
or realistic pipeline, employer-independent, plus the prospective-benefit mechanism (INA
203(b)(1)(A)(iii)) — opening with the firewall sentence that it clarifies and updates the record
and does not replace or materially alter the petition as filed. (2) **Totality narrative**, the
step-2 answer R6 expands: the arc across ≥2–3 distinct career periods, independent validators well
beyond the circle of personal and professional acquaintances, comparison against the TOP of the
frozen field. File it as an exhibit; it refreshes, never contradicts, the original.

## R6 Assemble → `rfe/response-letter.md` · `exhibit-index.md` · `package/`
Response letter, in the NOTICE's own order and headings. **Front matter**: a paragraph identifying
the notice date and receipt number; a NEW-exhibit index continuing the original numbering (N1,
N2…); and a SUMMARY TABLE — RFE concern → new evidence → exhibit number — from which the officer
can write the approval memo. **One section per finding**, each LEADING with new evidence
("Enclosed as New Exhibit N3 …"), tying old + new exhibits to the regulatory subsection, closing
with a one-line met-because sentence: the officer already read the original record and was not
persuaded, and bare re-argument is what denials quote back. **A dedicated FINAL MERITS section
last** (2–4 pages) even if the notice's step-2 language was brief — the sustained arc, the breadth
of independent validators, and the Policy Manual positive factors from `drafting.md` §3 rebuilt
around the challenged finding (field-normalized percentiles, not raw counts; the Carnegie/QS page
filed as an exhibit), plus any withdrawal sentences. **Tone**: "We respectfully submit…", never
"the Service erred". **The exhibit index QUOTES the notice sentence each new exhibit answers.**
Run `drafting.md`'s lint and re-check every count in case.json — counts drift between filing and
RFE. Submission (verify each against the notice; mechanics as of 2026-08):
- **Paper is the default** — I-140 is not online-filable (USCIS Forms Available to File Online,
  07/24/2026). Send to the address printed on the NOTICE (never a lockbox), with the premium
  coversheet (if the notice includes one) and then the ORIGINAL notice as the top pages — shipping
  evidence without them delays processing and can draw a denial. Offer online upload only if the
  user's myUSCIS account actually shows this RFE with a respond/upload option (received = its
  e-filing timestamp).
- **Premium**: E11 is premium-eligible at **15 business days**; the notice stopped the clock and a
  FRESH full period starts when USCIS receives the response (8 CFR 106.4(f)(3)). Filing or
  upgrading I-907 with the response forces action — but I-907 for an I-140 is **paper-only** (no
  online upgrade exists): send it to the address on the uscis.gov/i-907 direct-filing chart, which
  is not necessarily the RFE response address. Fee $2,965 as of 2026-03-01 — re-check the current
  G-1055 before quoting it. On REGULAR processing the post-response wait is unbounded — weeks to a
  year, 3–8 months typical for an I-140; promise no timeline, and name the upgrade as the only
  lever.
- **Delivery checklist** back from the received-by date: one complete shipment, coversheet (if any)
  then the ORIGINAL notice on top, then the response letter; tracked courier with signature,
  delivery 5–7 days early, full copy kept, tracking + delivery confirmation in STATE.md.
- Missing the deadline → denial as abandoned, on the record, or both (103.2(b)(13)(i)); an
  abandonment denial **cannot be appealed** — only a 103.5 motion to reopen. After ANY denial the
  I-290B clock is **30 days from the decision date** (33 if mailed; 15/18 to appeal a revocation),
  cannot be extended, and runs while the user hunts for counsel: say that date out loud and tell
  them to engage an attorney now. I-290B is $800, paper-only, no premium; motion vs AAO appeal vs
  refile is attorney territory, and say so.

## R7 Contribute (OPTIONAL — always ask, never assume)
After the response ships (or the decision arrives), offer once — if declined, drop it: an anonymous
data point + improvement suggestions to the project's benchmark. Fields (the GitHub issue-form
field ids — the contract): `category` · `field` · `citations` · `publications` · `filing_month`
(YYYY-MM) · `premium` · `rfe` · `outcome` · `processing_days` · `suggestion`; the form requires
category, field, citations, filing_month, rfe, outcome. Dropdown values must match the form's
option text EXACTLY — the prefill silently DROPS anything else — category `NIW|EB1A|EB1B|O1|Other`
(always `EB1A` here); premium `No | Premium from filing | Upgraded mid-case | Prefer not to say`;
rfe `No RFE | RFE received — overcame (approved) | RFE received — denied | NOID received | Prefer
not to say`; outcome `Approved|Denied|Withdrawn|Still pending`; `field` is one of the form's own 16
discipline buckets (last: `Other fields`) — if that list is not in front of you, leave `field` OUT
of the URL rather than guess; the form makes the user pick it.
**Anonymization is absolute**: no name, email, receipt/case number, employer, recommender names,
or institution if identifying — not even if the user offers them. Compose the values, SHOW them to
the user, get explicit approval; nothing goes out without a go-ahead. Then submit, in order:
(1) `gh` present and authenticated (`gh auth status`) → `gh issue create --repo HHHHHejia/openniw
--title "[data] case outcome" --label data-point --body <approved body>` (`--repo` is mandatory —
the case folder is never the project repo); (2) otherwise the prefilled form URL
`https://github.com/HHHHHejia/openniw/issues/new?template=data-point.yml&category=EB1A&citations=<v>&…`
(URL-encode values) for the user to sign in, tick the anonymization box and submit; (3) neither
works → print the ready-to-paste body.

Sources: 8 CFR 103.2(b)(8)–(16), 103.5, 106.4, 205.2 (eCFR); USCIS Policy Manual Vol. 1 Pt. E Ch. 6
(RFE/NOID rules) and Vol. 6 Pt. F Ch. 2 (two-step, final-merits factors); uscis.gov pages for
i-290b (06/01/2026), i-907 and Forms Available to File Online (07/24/2026); G-1055 (ed. 05/29/26);
the USCIS I-140 E11 RFE template (uscis.gov legal-docs) for deficiency headers — all verified
2026-08-03, re-verify fees and addresses before filing. AAO dismissal patterns 2024–2026 via
millermayer.com and greencard.writewing.in; intake, root-cause and withdrawal patterns adapted
from juntoku9/claude_immigration_attorney (MIT).
