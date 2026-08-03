# Stage IV–V — Official Forms & the Filing Package

## Workflow

1. `openniw fetch-forms` (fallback: `scripts/fetch_forms.py forms/blank`) —
   downloads official PDFs (I-140, ETA-9089 Appendix A + Final
   Determination, G-1145, I-907, G-1450, G-1650). The DOL (ETA-9089)
   downloads often 403 for scripts: if they fail, fetch those two PDFs with
   your own web tool or have the user download them from
   dol.gov/agencies/eta/foreign-labor/forms into forms/blank/.
2. Pre-fill `forms/answers.json` from case.json (key reference below) and
   list every derived key in `forms/answers.meta.json` `ai_keys`. Identity
   numbers, dates, and addresses must never be guessed — interview for
   them or leave the keys absent for the user to add in the wizard.
3. **Preferred**: launch the browser wizard — `openniw ui forms` (see
   SKILL.md Browser sessions). The user reviews amber AI fields, completes
   the rest, clicks Fill per form (live PDF preview), then Done. After
   Done: `openniw fill all` as the final deterministic pass.
   **Fallback** (no browser/companion): confirm every value in chat, then
   `pip install pypdf cryptography` + 
   `scripts/fill_form.py forms/answers.json all forms/blank forms`.
4. Review each filled PDF with the user; the report lists unmatched
   fields — anything unmatched gets filled by hand in a PDF viewer. I-907,
   G-1450 and G-1650 are downloaded but NOT script-fillable — complete them
   by hand. Always PRINT the filled forms and verify every page on paper
   before signing; do not trust a single on-screen viewer.

## answers.json key reference (flat semantic keys)

- `beneficiary.*`: family_name, given_name, middle_name, dob (MM/DD/YYYY),
  city_of_birth, state_of_birth, country_of_birth, citizenship, a_number,
  ssn, uscis_account
- `native_name.*`: family, given, middle (non-Roman alphabets only)
- `mailing.*`: street, apt, city, state (2-letter), zip, province,
  postal_code, country — U.S. residence at filing; no P.O. boxes
- `contact.*`: daytime_phone, mobile_phone, email
- `us_presence.*`: in_us (bool), date_of_arrival, i94_number,
  passport_number, passport_country, passport_exp, travel_doc_number,
  current_status
- `processing.*`: adjustment (bool), country_of_residence, consulate_city,
  consulate_country, prior_petition (bool), in_proceedings (bool),
  premium (bool — I-907; drives the lockbox address and package contents,
  never written into a PDF)
- `foreign_address.*`: street, city, province, postal_code, country
- `employment.*`: job_title, soc_code (e.g. "15-2051"), soc_title,
  job_description, full_time, permanent, new_position, wages, wages_per, hours
- `petitioner.*`: occupation, annual_income, nonprofit (bool),
  small_employer (bool, default true — sets the Asylum Program Fee answer)
- `degrees`: list of {level: doctorate|master|bachelor|associate|other,
  other_label (names the degree when level=other), field, institution,
  country, month_year (MM/YYYY, conferral date)}
- `current_employer`: {name, address1, address2, city, state, postal_code,
  country, job_title, start (MM/YYYY), end, hours_per_week, duties}
- `family`: list of {family_name, given_name, middle_name, dob,
  country_of_birth, relationship} — spouse + all unmarried children under 21

## Form-specific guidance (from firm practice)

- I-140 Part 2 for NIW = box 1.h on the current edition (the script sets
  the right checkbox; verify the label when reviewing). Part 5 = Self.
- Occupation ≠ job title: an occupation reflecting overall work/research
  (e.g. "Research Scientist"). Annual income = salary + cash bonus only.
- Nontechnical job description: <200 characters, plain language, research
  duties emphasized, NO employer/project/region names, NO teaching duties
  (officers rarely view teaching as nationally important).
- SOC code: what USCIS uses at the I-485 stage to check "same or similar
  field" — look it up at onetonline.org; choose deliberately.
- Processing: if unsure between adjustment and consular, consular is easier
  to change later than the reverse.
- Concurrent I-485 is a Visa Bulletin question. Aug 2026 Final Action Dates:
  EB-2 Worldwide Current — and DOS itself warns retrogression or
  unavailability may follow within months; China 09/01/2021; India
  Unavailable (FY2026 numbers exhausted; none before FY2027 opens
  2026-10-01). Check the current month's bulletin (travel.state.gov → Visa
  Bulletin) BEFORE advising concurrent filing.
- ETA-9089 Appendix A education: highest U.S. advanced degree relevant to
  the endeavor, or an evaluated foreign equivalent. Use the diploma's
  conferral date; the transcript's "Plan/Major" wording for the field.
- Final Determination page: DOL fields stay blank for NIW. Per the USCIS
  I-140 initial-evidence checklist, Appendix A and the Final Determination
  are signed by the petitioner AND the beneficiary — a self-petitioner signs
  BOTH blocks. Wet signatures, black ink.
- Priority date for NIW = the date USCIS receives the properly completed,
  signed I-140 with the correct fee (there is no DOL step).

## Fees & payment mechanics (verified 2026-08-02 — re-verify at uscis.gov)

I-140 $715 + Asylum Program Fee $300 (self-petitioner, ≤25 full-time U.S.
employees) = $1,015 — as TWO SEPARATE payments of the SAME payment type
(USCIS: packages "filed with more than one type of payment may be
rejected"). The fee questions drive I-140 Part 1: self-petitioner ⇒ Q5 = No,
Q6 = Yes; leaving Q5/Q6 blank ⇒ rejection, as does a wrong fee.
Optional premium processing (I-907) $2,965 — effective 2026-03-01 (Federal
Register doc 2026-00321); the E21 NIW premium clock is 45 BUSINESS days
(not the 15 that applies to most other I-140 classifications) and stops on
RFE issuance. The I-907 fee needs its OWN payment form. Payment is
electronic: G-1650 (ACH, recommended) or G-1450 (card; a declined card
rejects the entire package) — or G-1651 if paper-payment exempt.

## Filing channel — paper by mail is the default deliverable

A standalone, regular-processing I-140 can alternatively be filed ONLINE
through a USCIS online account (both options listed at uscis.gov/i-140,
verified 2026-08-02): the same package uploads as PDFs, the fee is paid
online, the receipt is an IOE number. Paper remains mandatory for
premium-at-filing (I-140 + I-907 together) and for concurrent I-140 + I-485
packages. Premium may be ADDABLE online later (standalone I-907 by PDF
upload) once an IOE receipt exists — but SOURCES CONFLICT: USCIS "Forms
Available to File Online" (07/24/2026) lists I-907 for an I-140 as
paper-only. Verify that page AND the uscis.gov/i-907 direct-filing chart
before choosing a channel, and default to paper; the same conflict is
flagged in `rfe-response.md` R6, where a premium upgrade filed with an RFE
response is the only speed lever. Online filers reuse the assembly order
below as the upload order; the lockbox tables apply to paper only.

## Assembly & mailing rules

Assembly order (top to bottom — USCIS recommends the payment form FIRST):
payment form(s) → G-1145 → I-907 (premium only, signed) → cover letter
(marked "Original Submission — Form I-140"; mark the envelope the same way)
→ signed I-140 → ETA-9089 Appendix A + signed Final Determination → foreign
name & address page (native alphabet, only if non-Roman; not needed if born
in India) → identity documents (passport pages with stamps, status approval
notice, I-94 front and back) → Petition Letter → signed PES → signed support
letters, each recommender's CV (max 5 pages) or bio page behind their letter
→ exhibits in Index order (publications: first 3-5 pages per paper, name
highlighted in the author list).

Rules from USCIS "Tips for Filing Forms by Mail": single-sided 8.5x11; no
staples, binders, or folders; black ink; typed entries Courier New 10 bold;
NEVER highlighter or correction fluid on a form (start the page over) —
highlighting names in evidence exhibits is fine and standard; same form
edition on every page with edition date/page numbers visible; number
supporting pages ("page 3 of 11"); any foreign-language document needs a
full English translation + the translator's signed certification; mark
copies of prior filings "COPY"; FedEx must use "Direct Signature Required"
(lockboxes reject "Adult Signature Required"); RFE responses go to the
address in the RFE letter, never a lockbox. Keep a complete copy.

## Where to mail (state lists verified 2026-08 — re-check before mailing)

By the state where the beneficiary will work:

- **Standard I-140** — Chicago Lockbox for CT DE DC IL IN IA KS ME MA MI MN
  MO NE NH NJ NY ND OH PA RI SD VT WI (USPS: USCIS, Attn: I-140, P.O. Box
  88774, Chicago, IL 60680-1774; courier: Attn: I-140 (Box 88774), 131 S.
  Dearborn St., 3rd Floor, Chicago, IL 60603-5517). **All other states →
  Dallas Lockbox** (USPS: USCIS, Attn: I-140, P.O. Box 660128, Dallas, TX
  75266-0128; courier: Attn: I-140 (Box 660128), 2501 S. State Hwy. 121
  Business, Suite 400, Lewisville, TX 75067-8003).
- **Premium (I-140 + I-907)** — Phoenix Lockbox for AK AZ AR CA CO GA GU HI
  ID LA MH MT NV NM MP OK OR TX VI UT WA WY + Armed Forces (USPS: USCIS,
  Attn: Premium I-140, P.O. Box 21500, Phoenix, AZ 85036-1500; courier:
  Attn: Premium I-140 (Box 21500), 2108 E. Elliot Rd., Tempe, AZ
  85284-1806). **All other states → Elgin Lockbox** (USPS: USCIS, Attn:
  Premium I-140, P.O. Box 4008, Carol Stream, IL 60197-4008; courier: Attn:
  Premium I-140 (Box 4008), 2500 Westfield Drive, Elgin, IL 60124-7836).
- **Concurrent I-140 + I-485, no premium** — any state: Dallas Lockbox,
  Attn: NFB, P.O. Box 660867, Dallas, TX 75266-0867 (courier: Attn: NFB
  (Box 660867), 2501 S. State Highway 121 Business, Suite 400, Lewisville,
  TX 75067-8003).

## Cover letter

One page, on top of the forms: USCIS lockbox address block; bold title
"Form I-140 (EB-2 National Interest Waiver) — Original Submission" (or "—
Premium Processing Request" when filing I-907); one paragraph — filed by the
self-petitioner under EB-2 with a request for a National Interest Waiver
pursuant to INA §203(b)(2)(B) and 8 C.F.R. §204.5(k), satisfying Matter of
Dhanasar, 26 I&N Dec. 884 (AAO 2016); a numbered ENCLOSED DOCUMENTS list in
physical package order ending with "Supporting Evidence (tabbed and
indexed)"; "Respectfully submitted," + name + "Self-Petitioner".

Sources: uscis.gov/i-140 · USCIS I-140 fee-payment alert (rel. 2024-09-23) ·
uscis.gov "How Do I Request Premium Processing" · federalregister.gov doc
2026-00321 · USCIS Direct Filing Addresses for Form I-140 ·
travel.state.gov Visa Bulletin (August 2026). All checked 2026-08-02;
volatile facts are stamped above — re-verify before filing.
