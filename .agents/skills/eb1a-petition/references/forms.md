# Stage IV–V — Official Forms & the Filing Package

EB-1A files NO Department of Labor paperwork: no ETA-9089, no Appendix A,
no Final Determination page, and no ability-to-pay evidence for a
self-petitioner. The package is forms + petition letter + statement +
letters + exhibits.

## Workflow

1. `openniw fetch-forms` (fallback: `scripts/fetch_forms.py forms/blank`)
   downloads official blank PDFs. Keep i-140.pdf, i-907.pdf, g-1145.pdf,
   g-1450.pdf, g-1650.pdf; the CLI also fetches ETA-9089 PDFs, which are
   not filed for this category — delete them from forms/blank/ (the
   bundled fallback script does not download them).
2. **`openniw fill` is NIW-only — never run it here.** Its I-140 mapping
   auto-checks Part 2 box 1.h (NIW) and fills ETA-9089 forms; an EB-1A
   filing needs box 1.a and no ETA forms. There is no browser forms
   wizard for EB-1A yet; the flow is chat interview → worksheet →
   hand-fill.
3. Interview the user and record every answer in `forms/worksheet.md`,
   grouped by form part (guide below). Identity numbers (A-Number, SSN,
   I-94, passport), dates, and addresses are never guessed — ask, or
   leave `[TODO]`. Values already in case.json are proposed for
   confirmation, never silently assumed.
4. The user completes each PDF by hand in a PDF viewer/editor from the
   worksheet; review the result together page by page. Always PRINT the
   filled forms and verify every page on paper before signing.

## I-140 field guide (E11; edition 06/07/24)

Verify the current edition and fee at uscis.gov/i-140 before filing —
USCIS rejects wrong-edition and wrong-fee packages.

- **Part 1 (petitioner)** = the self-petitioner: family/given name,
  mailing address (U.S. residence at filing; no P.O. boxes). EIN/SSN in
  Part 1 is NOT required for E11 (rejection-trigger exemption).
  **Question 5 = "No"**, **Question 6 = "Yes"** (self-petitioner /
  employs ≤25 full-time equivalents) — these two answers set the reduced
  $300 Asylum Program Fee tier; wrong answers cause fee-mismatch
  rejection.
- **Part 2 — check box 1.a "An alien of extraordinary ability"** (E11).
  Exactly one box. (1.h is NIW; 1.b is outstanding professor/researcher —
  do not confuse.)
- **Part 3 (beneficiary)** = the same person: full name, other names
  used, date/city/country of birth, citizenship, A-Number/SSN if any,
  and — if in the U.S. — date of arrival, I-94 number, passport details,
  current status.
- **Part 4 (processing)**: adjustment of status vs consular processing;
  if unsure, consular is easier to change later than the reverse.
  China/India-born petitioners usually cannot file I-485 concurrently
  (EB-1 retrogression — check the current visa bulletin). Answer the
  prior-petition and proceedings questions truthfully.
- **Part 5**: petitioner type = Self. Occupation ≠ job title — a label
  reflecting the overall work ("Research Scientist"); annual income =
  salary + cash bonus only.
- **Part 6 (basic proposed employment)**: job title, SOC code (look it up
  at onetonline.org — USCIS uses it at the I-485 stage for "same or
  similar" checks), nontechnical duties description <200 characters in
  plain language, full-time/permanent, wages, U.S. work location. For a
  self-petitioner without a fixed offer, describe the intended employment
  consistently with the statement's intent scope.
- **Part 7 (family)**: spouse and all unmarried children under 21.
- **Part 8 signature**: wet ink, black; typed names/stamps/pasted images
  are rejected. Date of birth (Part 3) and signature are
  rejection-trigger fields.
- **G-1145** (e-notification): name, email, mobile — clip to the front.
- **I-907** (optional premium processing): E11 premium = **15 business
  days** to adjudicative action (approval, denial, NOID, or RFE; the
  clock resets after an RFE response). Fee **$2,965** (since 2026-03-01),
  paid with its OWN payment form — one payment per form, never combined.
  Complete by hand; signed.

## Fees & assembly (2026 — verify at uscis.gov/g-1055 before mailing)

I-140 $715 (paper) + Asylum Program Fee $300 (self-petitioner tier) =
**$1,015** — as TWO SEPARATE payments of the SAME payment type (USCIS:
provide separate payments; packages "filed with more than one type of
payment may be rejected"). With premium, the $2,965 I-907 fee is a THIRD
separate payment on its own payment form: $3,980 total across three
payments. Payment is electronic: G-1650 (ACH, recommended) or G-1450
(card; a declined card rejects the entire package).

**Filing channel** — paper by mail is the ONLY channel: the I-140 is not
online-filable, and neither is an I-907 for an I-140 (USCIS "Forms
Available to File Online", updated 07/24/2026 — re-check there before
filing). A paper case receipted into the electronic system gets an **IOE**
receipt number, which lets the user later link the case to a myUSCIS
account for notices and — if the case is processed electronically — for
uploading an RFE response. The lockbox tables below govern every filing.

Assembly order (top to bottom — USCIS recommends the payment form FIRST):
payment form(s) → G-1145 → I-907 (premium only, signed) → cover letter
(marked "Original Submission — Form I-140"; mark the envelope the same
way) → signed I-140 → identity documents (passport pages with stamps,
status approval notice, I-94 front and back; foreign name & address page
in the native alphabet if non-Roman, not needed if born in India) →
Petition Letter → signed intent-to-continue-work statement → signed
support letters, each recommender's CV (max 5 pages) or bio page behind
their letter → exhibits in Index order, tabbed (publications: first 3-5
pages per paper, name highlighted in the author list).

Rules from USCIS "Tips for Filing Forms by Mail": single-sided 8.5x11; no
staples, binders, or folders; black ink; NEVER highlighter or correction
fluid on a form (start the page over) — highlighting names in evidence
exhibits is fine and standard; same form edition on every page with
edition date/page numbers visible; number supporting pages ("page 3 of
11"); any foreign-language document needs a full English translation +
the translator's signed certification; mark copies of prior filings
"COPY"; FedEx must use "Direct Signature Required" (lockboxes reject
"Adult Signature Required"); RFE responses go to the address in the RFE
letter, never a lockbox. Keep a complete copy. Priority date = the date
USCIS receives the properly completed, signed I-140 with the correct fee.

## Where to mail (state lists verified 2026-08 — re-check before mailing)

USCIS moves lockboxes; re-check the I-140 direct-filing-addresses page.
By the state where the beneficiary will work. **CRITICAL: the premium
split is NOT the standard split** — e.g. FL/GA/LA/TX all go to Dallas
standard, but FL goes Elgin and GA/LA/TX go Phoenix for premium. Pick the
table for what is actually in the envelope.

- **Standard I-140 (no I-907)** — Chicago Lockbox for CT DE DC IL IN IA
  KS ME MA MI MN MO NE NH NJ NY ND OH PA RI SD VT WI (USPS: USCIS, Attn:
  I-140, P.O. Box 88774, Chicago, IL 60680-1774; courier: Attn: I-140
  (Box 88774), 131 S. Dearborn St., 3rd Floor, Chicago, IL 60603-5517).
  **All other states → Dallas Lockbox** (USPS: USCIS, Attn: I-140, P.O.
  Box 660128, Dallas, TX 75266-0128; courier: Attn: I-140 (Box 660128),
  2501 S. State Hwy. 121 Business, Suite 400, Lewisville, TX 75067-8003).
- **Premium (I-140 + I-907, with or without I-485)** — Elgin Lockbox for
  AL CT DE DC FL IL IN IA KS KY ME MD MA MI MN MS MO NE NH NJ NY NC ND OH
  PA PR RI SC SD TN VT VA WV WI (USPS: USCIS, Attn: Premium I-140, P.O.
  Box 4008, Carol Stream, IL 60197-4008; courier: Attn: Premium I-140
  (Box 4008), 2500 Westfield Drive, Elgin, IL 60124-7836). **All other
  states → Phoenix Lockbox** (USPS: USCIS, Attn: Premium I-140, P.O. Box
  21500, Phoenix, AZ 85036-1500; courier: Attn: Premium I-140 (Box
  21500), 2108 E. Elliot Rd., Tempe, AZ 85284-1806).
- **Concurrent I-140 + I-485, no premium** — any state: Dallas Lockbox,
  Attn: NFB, P.O. Box 660867, Dallas, TX 75266-0867 (courier: Attn: NFB
  (Box 660867), 2501 S. State Highway 121 Business, Suite 400,
  Lewisville, TX 75067-8003).
- **Upgrading a pending I-140 later**: a standalone I-907 is PAPER-ONLY
  (there is no online I-907 for an I-140, whatever the receipt number) and
  goes to the Elgin/Phoenix I-907 boxes as listed 2026-08 — verify on the
  uscis.gov/i-907 direct-filing chart before mailing.

## Cover letter

One page, on top of the forms: USCIS lockbox address block; bold title
"Form I-140 (EB-1A, Alien of Extraordinary Ability) — Original
Submission" (add "— Premium Processing Request" when filing I-907); one
paragraph — filed by the self-petitioner under INA §203(b)(1)(A) and
8 C.F.R. §204.5(h), initial evidence satisfying at least [N] of the ten
criteria at 8 C.F.R. §204.5(h)(3) plus evidence of intent to continue
work in the area of expertise; a numbered ENCLOSED DOCUMENTS list in
physical package order ending with "Supporting Evidence (tabbed and
indexed)"; "Respectfully submitted," + name + "Self-Petitioner".

Sources: uscis.gov/i-140 (form + edition + filing tips), USCIS "Forms
Available to File Online" (updated 07/24/2026 — I-140 and I-907-for-I-140
absent), USCIS G-1055 fee schedule (ed. 05/29/26), USCIS I-140
fee-payment alert (rel. 2024-09-23, separate-payments rule), USCIS I-140
and I-907 direct filing addresses pages (last
reviewed 04/08/2025, fetched 2026-08), USCIS E11 initial-evidence
checklist, Federal Register 2026-00321 (premium fee $2,965 eff.
2026-03-01). All figures re-verifiable on uscis.gov before filing.
