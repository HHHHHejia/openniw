# Stage IV–V — I-129, Fees, Assembly & the Petitioner Hand-off

## Workflow

1. `python3 scripts/fetch_forms_o1.py` — downloads blank I-129, I-907,
   G-1145 into `forms/blank/` (the O and P Classifications Supplement is
   inside the I-129 package). Do NOT use `openniw fetch-forms` (NIW form
   set), `openniw fill`, or `openniw ui forms` (both hardwired to NIW's
   I-140/ETA-9089 field maps — a browser wizard for O-1 is roadmap).
2. Verify the edition: I-129 edition 02/27/26 as of this skill's last
   review — USCIS rejects outdated editions; confirm at uscis.gov/i-129
   and check every page shows the same edition date.
3. Work field-by-field in chat: walk the form in PDF order with the guide
   below, record every confirmed answer in `forms/worksheet.md` (grouped
   by form part, quoting the field label), and have the user (or their
   petitioner) type answers into the PDF. Never guess identity numbers,
   dates, or addresses — interview or leave `[TODO]`. Print and verify
   every page on paper before signatures.

## Who is who (get this wrong and the filing fails)

- **Petitioner** = the employer / agent / beneficiary-owned entity from
  petition-frame.md — NEVER the beneficiary personally. The petitioner's
  legal name, address, FEIN, and signatory go in the petitioner sections;
  the petitioner SIGNS the I-129 declaration (and the I-907 if premium).
  The beneficiary signs nothing on the I-129 itself.
- **Beneficiary** = the applicant: identity, birth, citizenship, passport,
  I-94/status data. One beneficiary per O-1 petition; O petitions are
  paper-filed (no online I-129 for O as of 2026).

## I-129 + O/P supplement field guide (walk in this order)

- **Petitioner information**: legal entity name exactly as registered;
  mailing address; FEIN; entity type; year established, employee count,
  income — from case.json entity facts. Founder cases: the company is
  the petitioner; the signatory is an authorized officer (per the
  governance package, ideally not the beneficiary).
- **Requested classification**: "O-1A". Requested dates of employment:
  the frozen validity window, ≤3 years, matching the itinerary and
  contract exactly.
- **Requested action** — decide with the user: change of status (in the
  U.S. in valid status; no O-1 work until approval) vs consular
  notification. If OPT/current status expires while a COS is pending, the
  beneficiary may stay but CANNOT work until approval — there is no
  cap-gap for O-1; premium filing before the gap is the standard play.
- **Beneficiary information**: names as in passport; other names used;
  birth data; nationality; passport number/expiry; current U.S. status,
  I-94 number, SEVIS if F/J — never guessed.
- **Employment details**: job title and a plain-language duties summary
  (each duty inside the frozen field label); work address(es) — must
  match the itinerary; wage as in the contract.
- **O/P Classifications Supplement**: classification O-1A; the event
  dates; consultation information (which entity/expert provided the
  advisory opinion, or the no-peer-group statement); prior O-1 stays if
  any. Follow the supplement's own instructions line by line — editions
  move fields around; the form instructions PDF is authoritative.
- **Declarations/signatures**: petitioner signatory signs, wet signature,
  black ink; preparer/interpreter sections completed truthfully (the user
  prepared it; you are software assistance, not a preparer).
- **I-907** (premium, strongly recommended — see fees): petitioner as on
  the I-129; the O-1 premium clock is 15 business days, resets on RFE; a
  standalone online I-907 upgrade works later for a pending IOE receipt.
- **G-1145**: e-notification of acceptance; clip to the top form.

## Fees (2026 schedule — verify at uscis.gov/g-1055 before mailing)

| Item | Regular employer | Small employer (≤25 FTE in the U.S., incl. affiliates) | Nonprofit |
|---|---|---|---|
| I-129 base fee (O) | $1,055 | $530 | $530 |
| Asylum Program Fee | $600 | $300 | $0 |
| **Total without premium** | **$1,655** | **$830** | **$530** |
| I-907 premium (optional) | +$2,965 | +$2,965 | +$2,965 |

Premium is $2,965 for filings postmarked on/after 2026-03-01. Pay each
fee with a SEPARATE check from the petitioner (USCIS rejects some
combined payments); the size/nonprofit answers on the form must match the
fee paid. Later, at the visa stage: DS-160 MRV fee $205; a ~$250 "visa
integrity fee" at issuance was enacted in 2025 but rollout is uneven —
verify on travel.state.gov.

## Where to mail

All I-129s go to a USCIS lockbox, split by the PETITIONER's primary
office state (roughly northern-tier states → Chicago, southern-tier →
Dallas), and premium-inclusive filings use DIFFERENT PO boxes at the same
lockboxes. Do not trust a hardcoded address: pull the exact "O
classifications" address (premium vs non-premium) from
uscis.gov/i-129-addresses at assembly time and paste it into the cover
letter and envelope. FedEx: "Direct Signature Required" (lockboxes reject
"Adult Signature Required"). RFE responses go to the address in the RFE
letter, never a lockbox.

## Assembly order (top to bottom)

payment check(s) → G-1145 → I-907 (premium only, signed) → cover letter →
signed I-129 with O/P supplement → consultation/advisory opinion
(watermarked original if issued that way) → contract or oral-agreement
summary → itinerary/event explanation → petitioner documents (corporate/
governance package, or agent authorizations + per-employer contracts) →
support letter → expert letters, each signer's CV (max 5 pages) behind
their letter → beneficiary identity/status documents (passport bio page,
I-94, current status evidence, degrees) → exhibits in Index order.

USCIS mail rules: single-sided 8.5x11; no staples, binders, or folders;
black ink; never highlighter or correction fluid ON a form (highlighting
names in evidence exhibits is fine); number supporting pages ("page 3 of
11"); certified English translations for any foreign-language document;
mark copies "COPY". Keep a complete copy of everything.

**Cover letter** (one page, petitioner's letterhead): lockbox address
block; bold title "Form I-129 — Petition for O-1A Nonimmigrant Worker —
Original Submission" (add "— Premium Processing Request" if I-907);
one paragraph naming petitioner, beneficiary, classification O-1A, field,
and validity dates; a numbered ENCLOSED DOCUMENTS list in physical
package order; "Respectfully submitted," + signatory name/title.

## Stage V — the petitioner hand-off (documents/handoff.md)

The deliverable is a kit the petitioner can execute without research:
1. **What they receive**: the assembled package + this hand-off memo.
2. **What they sign** (flag each line with a tab): I-129 declaration, O/P
   supplement where required, I-907, support letter, cover letter; plus
   checks for each fee.
3. **What they verify before signing**: entity facts, wage, dates —
   against their own records, not just case.json.
4. **Mail** to the freshly pulled lockbox address; file no more than
   1 year and ideally at least 45 days before the start date.
5. **After filing**: receipt notice (I-797C) → any RFE goes to rfe.md →
   approval (I-797). COS approvals take effect on the notice. Consular
   route: DS-160, in-person interview (waivers for O-1 effectively ended
   late 2025 — practitioner-reported; expect possible 221(g) processing
   and immigrant-intent probing — O-1 is only quasi-dual-intent), and a
   stamping kit: original I-797, full petition copy, employment
   verification letter, (founders) proof the company is real and
   operating. Canadians are visa-exempt: I-797 at the port of entry.

## Dependents & status practicalities (tell the user unprompted)

- **O-3** (spouse + unmarried children under 21): same admission period;
  study is fine; **no work authorization under any circumstances — there
  is no O-3 EAD** (unlike H-4/L-2); dual-career couples need an
  independent status for the spouse. I-539 ($470 paper / $420 online)
  for COS/extension. **O-2** support staff exist only for athletics/arts
  O-1s — out of scope here.
- **Admission window**: validity plus up to 10 days before and after;
  work only inside the validity dates. **Grace**: up to 60 consecutive
  days (discretionary, once per validity period) if employment ends —
  not a guarantee in the current enforcement climate. Same-employer
  timely-filed extension: up to 240 days continued work authorization.
- **No cap, no lottery, no filing season** — file year-round; with
  premium this is the fastest extraordinary-ability route.
- **Extensions**: same event → ≤1-year increments; NEW event (a new
  project/phase, even same employer) → fresh up-to-3-year grant;
  unlimited extensions. Job/petitioner change → new (or amended, if
  agent-filed) petition BEFORE the new work begins.

Sources: uscis.gov/i-129, uscis.gov/i-129-addresses, uscis.gov/g-1055;
8 CFR part 106 (fees) and 8 CFR 214.2(o) via eCFR; 91 FR 1059 (premium
fee, 2026); travel.state.gov (MRV); consular-climate notes are
practitioner-reported (manifestlaw.com, lighthousehq.com) — verify.
