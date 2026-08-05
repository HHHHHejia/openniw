# Stage I — The Gate

Six mechanical checks, in order. Each has a published answer; each STOPS the
workflow when it fails. Report the result and the reason — never an opinion on
whether the user "should" be able to adjust. Output `eligibility.md` with an
as-of date on every volatile line.

## Gate 1 — the I-140 basis

Three filing timings exist:

| Timing | What proves the basis | Open to a self-filer |
|---|---|---|
| Concurrent with the I-140 | nothing (both in one submission) | **Yes, on paper** — 8 CFR 245.2(a)(2)(i)(B)-(C) authorize it for anyone whose I-140 is bundled in the same mailer, same day, same office. The **online** channel is the narrow one (Gate 6): concurrent online filing is open only to representatives and to unrepresented I-140 self-petitioners |
| I-140 pending | copy of the I-140 **receipt** notice (I-797C) | Yes |
| I-140 approved | copy of the I-140 **approval** notice (I-797) | Yes |

Rules:
- The basis evidence must be a copy of the **actual I-797 notice**. A case-status
  screenshot, a text alert, or a myUSCIS page is **not** acceptable. STOP and ask
  for the notice.
- Read off the notice and write into case.json: receipt number, preference
  category, **priority date**, beneficiary name exactly as printed.
- **Priority date** (8 CFR 204.5(d)): with no labor certification (EB-1A, NIW) it
  is the date the I-140 was properly filed — the receipt date, not the approval
  date. With PERM it is the date DOL accepted the labor certification. If the
  notice's printed priority date and the receipt date disagree, surface both and
  ask; never pick one silently.
- **Multiple approved I-140s** → the applicant is entitled to the **earliest**
  priority date (8 CFR 204.5(e)(1)). Claim it clerically: include the earlier
  approval notice in the package and say so in the cover letter. A **denied**
  petition establishes no priority date at all (204.5(e)(3)). Whether a
  *revoked* petition keeps its date turns on why it was revoked → **attorney**.
- Filing on a pending I-140 carries structural risk, stated plainly and not
  weighed for the user: the I-485 rides on the I-140, and if the I-140 is denied
  the I-485 falls with it and its fee is lost. No update to USCIS is needed when
  a pending I-140 is later approved — the adjudicator is notified internally.

## Gate 2 — the Visa Bulletin (re-run every single time; never cache)

All lookups are for the month USCIS will **RECEIVE** the package, not the month
you assemble it.

```
1. Open the USCIS page "Adjustment of Status Filing Charts from the Visa
   Bulletin". Read the EMPLOYMENT-BASED sentence for the target month.
   Not yet posted → STOP. Not determinable; do not mail. (USCIS posts within
   about a week of DOS publishing the bulletin.)
   Record: DESIGNATED = Final Action Dates | Dates for Filing.
2. Read BOTH employment-based charts for that month. Cell = (row: category,
   column: chargeability country).
3. Operative cutoff OP = the more favorable of {DESIGNATED cell, FAD cell}:
   if the FAD cell is "C", or is later than the DFF cell, FAD controls.
4. OP == "C"                       → may file
   OP == "U"                       → MAY NOT FILE (no priority date helps)
   priority date STRICTLY EARLIER than OP → may file
   priority date EQUAL to OP, or later    → MAY NOT FILE
5. Confirm delivery lands inside that month.
```

- The comparison is strictly earlier-than. A priority date equal to the cutoff is
  **not** current (8 CFR 245.1(g)(1)).
- The chart designation is made **separately for family-sponsored and
  employment-based** and they routinely differ. Read the EB sentence only.
- **Chargeability = country of BIRTH**, not citizenship, residence, or passport
  (INA 202(b)). Read it off the birth certificate or passport. **Cross-
  chargeability** to a spouse's country of birth exists under INA 202(b)(2) and
  can rescue a backlogged principal. Detect the opportunity and say so. The
  **assembly is clerical and in scope** once the user confirms both spouses are
  independently eligible to adjust and both are filing: both I-485s in one family
  pack, the spouse's birth certificate with certified translation, the marriage
  certificate, and the explicit cover-letter request (`package.md`). The **hard
  stop** is the judgment — the marriage's bona fides or timing, or whether the
  spouse is independently eligible to adjust; asserting the claim puts the
  marriage at issue. Never available to a single applicant, from a child to a
  parent, or where the spouse is not filing.
- Fetching: the USCIS designation page and its "When to File …" page (which
  reproduces the designated chart) are retrievable. **travel.state.gov is
  Cloudflare-blocked to agents** — when non-designated chart values matter, ask
  the user to open the DOS bulletin in a normal browser and paste both EB tables.
  Law-firm summaries are a cross-check, never a source of record.
- **A second calendar fact the user should have at intake: 2026-09-18.** The 2022
  public-charge regulation is rescinded that day; applications postmarked or
  e-submitted **on or after** it need the revised I-485 edition and are judged
  under the restored discretionary totality-of-circumstances public-charge test.
  State the date and which side of it the target filing month falls on. **Do not
  advise on whether to beat it** — that trade-off is the user's.
- **Rejection destroys the filing date.** A package received in a month when the
  category is not current is rejected, and rejected applications do not retain a
  filing date. Conversely a package received inside a valid month is safe even if
  the category exhausts mid-month.
- **Not current → STOP the filing, not the work.** Useful preparation while
  waiting: obtain or repair the birth document (the longest lead time of
  anything), collect every I-20/DS-2019/I-797/I-94 and build the history files,
  gather five years of addresses and employment, resolve 212(e), replace a lost
  passport, keep the address current with USCIS — and hold off on the medical
  exam and on signing anything until a filing month is in sight.

## Gate 3 — INA 212(e), if there is ANY J-1 or J-2 history, ever

```
Ever held J-1 or J-2 (principal OR any derivative, however long ago)?
  NO  → nothing further
  YES → is that person subject to the two-year foreign residence requirement?
        NOT SUBJECT  → state it in the cover letter and attach the proof
                       (DOS advisory opinion, DS-2019, visa annotation)
        SUBJECT, SATISFIED → attach physical-presence proof
        SUBJECT, WAIVED    → attach the APPROVED I-612 approval notice
        ANYTHING ELSE      → HARD STOP
```

- 212(e) attaches when the program was financed by the U.S. government or the
  government of last legal residence; or the person's field appeared on the DOS
  Exchange Visitor Skills List for their country at the time; or the J status was
  for graduate medical education or training. Unsure → a DOS advisory opinion is
  the published route; file any advisory opinion ever received, either way.
- **Derivatives inherit the exposure.** If the J-1 was subject, J-2 dependents
  were too, and each needs their own copy of the waiver evidence. The common miss
  is clearing the principal and forgetting the spouse.
- A DOS favorable recommendation is **not** enough — USCIS wants its own approved
  I-612. The "file on a No Objection Statement before the I-612 is approved"
  route exists: **name it, refuse to recommend it, refer to counsel** — if the
  waiver is ultimately denied the I-485 is denied and the fee lost.
- Unresolved 212(e) is an outright ineligibility (8 CFR 245.1(c)(2)), not a
  paperwork gap. STOP the whole filing until it is resolved.

## Gate 4 — status posture (collect facts; do not analyze them)

Collect, per person: current status and its class; I-94 number and expiry (or
`D/S`); date and manner of last entry (inspected and admitted / inspected and
paroled / neither); whether they are physically in the United States now.

STOP and route to an attorney the moment any of these surfaces: a gap, an
overstay, an expired I-94, work without authorization of any length, a departure
without advance parole while an I-485 was pending, or uncertainty about whether an
entry was an inspection and admission. Do not attempt a 245(c) or 245(k) analysis.
You may say what INA 245(k) is — a limited employment-based exemption from three
adjustment bars, turning on an aggregate day count since the most recent lawful
admission — and then that the count is attorney work and that it forgives
adjustment bars only, not unlawful-presence inadmissibility. Physical presence in
the U.S. is required at filing; if the applicant is abroad, STOP.

## Gate 5 — derivatives

Only a **spouse** and **unmarried children under 21** qualify. Not parents, not
siblings, not married children, not children who have aged out — those are family
based and out of scope. The marriage must predate the principal's approval.

Collect into `applicants/` for each derivative: full legal name as in the passport,
DOB, country of birth, current status and I-94, relationship evidence (marriage or
birth certificate), and their own J history. Each derivative is a separate applicant
with a separate I-485, fee, medical exam and history file.

**Age-out**: if any child is within roughly 18 months of 21, say so immediately
and route the CSPA question to counsel. Collect the inputs — I-140 receipt date,
I-140 approval date, the child's DOB, the relevant bulletin month — and **compute
nothing**. A wrong CSPA answer silently costs a child their green card.
Dependents already abroad who must follow to join are a separate Form I-824
track; note it and route the timing question to counsel.

## Gate 6 — filing channel

| | Paper | Online (PDF upload into a USCIS account) |
|---|---|---|
| Who may — **concurrent** (I-485 + I-140 together) | anyone | representatives; and **unrepresented I-140 self-petitioners** (EB-1A, NIW). Nobody else |
| Who may — **sequential** (I-140 already filed) | anyone | representatives; and an **unrepresented applicant whose petitioner filed the I-140 online**, once the petitioner has received the I-140 acceptance notice — the I-485 then goes in through the applicant's own USCIS account. Everything else by mail |
| I-693 | sealed envelope goes in **unopened** | envelope **must be opened**, the I-693 uploaded, and the original form + envelope retained until a final decision |
| Fee | higher | about $50 lower per form for I-485 and I-131; I-765 (c)(9) is the same either way |
| Later advance parole online | **no** — online I-131 for a pending I-485 requires an I-485 receipt beginning `IOE`, which paper filings do not get | yes |

Two more: an I-140 filed with premium processing (I-907) forces paper for the
whole bundle; and never mix channels on one form — a printed copy of an online
form mailed to a lockbox is rejected. The channel is a **one-way door** on later
online advance parole: present the table, let the user choose, log it in STATE.md.
**Re-verify this table at channel-choice time** against
uscis.gov/file-online/forms-available-to-file-online — the eligible-filer list
moves without a form revision (read 2026-08-04).

## The output — eligibility.md

One page, in this order: filing basis and its notice · category and priority date
· chargeability country and the chart result with the month and the date checked ·
212(e) disposition per person · status facts collected (facts only) · derivative
roster · chosen filing channel · **gates passed / gates failed** · every hard stop
that tripped, with the fact that triggered it. Close with: this is a completeness
report, not an eligibility determination.

Sources: uscis.gov/i-485; USCIS "Adjustment of Status Filing Charts from the Visa
Bulletin" and "When to File …"; 8 CFR 204.5(d)-(e), 245.1(c)(2), 245.1(g),
245.2(a)(2); INA 202(b), 245(a), 245(k); USCIS Policy Manual Vol. 7 Pt. A Ch. 3,
6, 7 and Pt. B Ch. 5, 8; 22 CFR 41.62(c). Checked 2026-08-04.
