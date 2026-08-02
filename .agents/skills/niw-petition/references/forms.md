# Stage IV–V — Official Forms & the Filing Package

## Workflow

1. Run the skill's `scripts/fetch_forms.py forms/blank` — downloads official
   PDFs (I-140, ETA-9089 Appendix A + Final Determination, G-1145, I-907,
   G-1450, G-1650). The DOL (ETA-9089) downloads often 403 for scripts: if
   they fail, fetch those two PDFs with your own web tool or have the user
   download them from dol.gov/agencies/eta/foreign-labor/forms into
   forms/blank/.
2. Build `forms/answers.json` from case.json + an interview for what's
   missing (see key reference below). Confirm every value with the user —
   identity numbers, dates, and addresses must never be guessed.
3. `pip install pypdf cryptography` (one-time), then run the skill's
   `scripts/fill_form.py forms/answers.json all forms/blank forms`
4. Review each filled PDF with the user; the script reports unmatched
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
  consulate_country, prior_petition (bool), in_proceedings (bool)
- `foreign_address.*`: street, city, province, postal_code, country
- `employment.*`: job_title, soc_code (e.g. "15-2051"), soc_title,
  job_description, full_time, permanent, new_position, wages, wages_per, hours
- `petitioner.*`: occupation, annual_income, nonprofit (bool),
  small_employer (bool, default true — sets the Asylum Program Fee answer)
- `degrees`: list of {level: doctorate|master|bachelor|associate|other,
  field, institution, country, month_year (MM/YYYY, conferral date)}
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
  to change later than the reverse. India/China-born usually cannot file
  I-485 concurrently (retrogression).
- ETA-9089 Appendix A education: highest U.S. advanced degree relevant to
  the endeavor, or an evaluated foreign equivalent. Use the diploma's
  conferral date; the transcript's "Plan/Major" wording for the field.
- Final Determination page: DOL fields stay blank for NIW; the worker is
  identified and the petitioner signs it. Wet signatures, black ink.

## Fees & assembly (2026 — verify at uscis.gov before mailing)

I-140 $715 + Asylum Program Fee $300 (self-petitioner) = $1,015.
Optional premium processing (I-907) $2,965 — separate payment form.
Payment is electronic-only: G-1650 (ACH, recommended) or G-1450 (card; a
declined card rejects the entire package). One payment method per filing.

Assembly order (top to bottom): G-1145 clipped on top → payment form →
signed I-140 → ETA-9089 Appendix A + signed Final Determination → Petition
Letter → signed PES → signed support letters → exhibits in Index order.
Print single-sided; no staples; verify the current lockbox address at
uscis.gov/i-140 just before mailing. Keep a complete copy.
