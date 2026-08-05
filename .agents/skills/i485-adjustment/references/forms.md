# Stage III — Forms, Field by Field

**No machine filling.** This skill does not run `openniw fill` and offers no wizard: a machine mis-ticking a
Part 9 box is exactly the harm the skill exists to avoid (a guided wizard is roadmap). Work each form in
chat, one Part at a time, recording every confirmed answer in `forms/<person>-worksheet.md` by Part, quoting
the field label. The user types the answers in, prints, and checks every page on paper before signing.

## Before anything

1. Send the user to uscis.gov for **I-485** and, as applicable, **I-765**, **I-131**, **I-693**,
   **Supplement J**, **G-1145** and the payment form (`openniw fetch-forms` fetches the I-140 set — not
   usable here).
2. **Verify the edition date on each form's own USCIS page at fill time, every time.** A superseded edition
   is a rejection, not an RFE. A revised I-485 is expected as the 2022 public-charge regulation is rescinded
   effective **2026-09-18**, and older editions will not be accepted on or after that date — so re-read the
   form page before relying on any Part number below.
3. Confirm the same edition date and page number are visible at the **bottom of every page** and that all
   pages come from one edition — mixed or missing pages are a published rejection trigger. The I-485 is also
   a dynamic PDF whose per-page 2D barcodes regenerate as data is typed: fill and save in Adobe
   Reader/Acrobat before printing, and check a barcode appears on every printed page.

## Universal fill rules

- **Never blank.** Inapplicable prose/identity fields get `N/A`; numeric fields whose answer is zero get
  `None` — not `0`, not `N/A`. Reversing these two is a documented deviation.
- Black ink by hand, or typed in **Courier New 10 bold** (the only published font spec). Never highlighter
  or correction fluid **on a form** — a mistake means starting that page over (highlighting names in
  evidence exhibits is fine).
- Dates are **mm/dd/yyyy** everywhere; biographic measurements are **U.S. units only**. **"Other names used"
  is never blank** — `None`, or every variant ever used, including a full maiden name and the name reversed
  if any document ever rendered it that way.
- Name spelling, name order and date of birth are **card-printing fields**: an error means paying USCIS for
  a corrected card. Family name first. Overflow goes to the additional-information Part with each entry's
  Page / Part / Item reference; an extra sheet needs the name and A-Number at top, signed.

## Form I-485 — what each Part wants

| Part | Contents | EB note |
|---|---|---|
| Front matter | "For USCIS Use Only"; attorney block | **Leave both entirely blank.** Repeat the A-Number header on every page (blank if none) |
| 1 | Information About You | Legal name; every other name used since birth; DOB and any other DOB ever used; A-Number(s); sex; place of birth; citizenship; USCIS online account; passport/travel-document and visa data; **manner of last entry**; most recent I-94 and class of admission; current status and expiry; alien-crewman questions; current physical address with date first resided, mailing address, and **5 years of prior addresses**; most recent non-U.S. address lived in over a year; SSN block |
| 2 | Application Type or Filing Category | The removal-proceedings question — a **Yes is a hard stop**. The **I-140 receipt number and priority date**. Principal vs derivative. **Exactly one** category box under Employment-based (extraordinary ability / outstanding professor or researcher / multinational executive or manager / advanced degree or exceptional ability **not** seeking a waiver / professional / skilled worker / other worker / **national interest waiver**). Then the relative question — whether a relative filed the I-140 or holds ≥5% of the petitioning business; **self-petitioners take the N/A "adjusting on a self-petition" option**. Then Item 4, which asks whether the applicant is applying under **INA 245(i)** — do not supply an answer: anything other than a confident No from the user, and any Yes, is a hard stop (SKILL.md #17). Then the CSPA item |
| 3 | Affidavit-of-Support exemption request | Select exactly one — decision table below. Form I-864W is obsolete; this Part replaced it |
| 4 | Additional Information About You | Prior immigrant-visa application at a consulate and its outcome; prior application for permanent residence; LPR status ever rescinded; **all employment AND education for the last 5 years**, most recent first, including self-employment, unemployment and retirement with the **source of support** for every non-working period; most recent employer or school **outside** the U.S. |
| 5 | Parents | Both parents: legal name, name at birth if different, DOB, country of birth. No "if living" qualifier — deceased parents are still listed |
| 6 | Marital History | Marital status; number of times married (counting marriages abroad, annulments, remarriage to the same person); current-spouse block; prior-spouse block including how and where each marriage ended. Unmarried → `N/A` across the spouse blocks |
| 7 | Children | Total number of **all** living children anywhere in the world — biological, adopted and current stepchildren, any age, married or not, living with you or not — then a block per child. Zero → `None` |
| 8 | **Biographic Information** | Mechanical and harmless: ethnicity, race (all that apply), height, weight, eye and hair colour |
| **9** | **General Eligibility and Inadmissibility Grounds, Items 1–86** | **HARD-STOP ZONE — see below** |
| 10 | Contact, certification, signature | Phones, email, the perjury certification, signature and date |
| 11 / 12 | Interpreter / Preparer | Only if one was used; otherwise `N/A`. If anyone other than the applicant prepared the form, Part 12 is the honest place for it — the applicant decides what goes there |
| 13 | Signature at Interview | **Leave blank.** Signed in ink at the interview when the officer says so |
| 14 | Additional Information | Overflow, per the rules above |

**Renumbering warning**: in the current edition the inadmissibility block is **Part 9** and Part 8 is
harmless biographic data. An earlier edition numbered it Part 8, so an older checklist saying "the Part 8
questions" means this block. Always say Part 9, and explain the shift if the user has an old list.

## Part 9 — the protocol

The form's own instruction: answer Yes where Yes is correct, **and also explain any No you are unsure of**.
The seven blocks, named only — (a) organizations, associations and memberships anywhere in the world; prior
denial of admission or a visa; unauthorized work; status violations; removal proceedings and orders; the J
two-year requirement. (b) **Criminal Acts and Violations** — arrests, citations, charges, diversion and
convictions, **even if expunged, sealed, pardoned or dismissed**. (c) **Security and Related** — espionage,
weapons or military-type training, terrorist activity and support, service in a prison or in any military,
police or paramilitary unit, totalitarian-party membership, torture, genocide, child soldiers. (d) **Public
Charge** — an exempt-category selector an ordinary EB applicant does not fall into, then household size,
income, assets, liabilities, education, skills, and receipt of cash income-maintenance benefits or long-term
institutionalization at government expense. (e) **Illegal Entries and Other Immigration Violations**. (f)
**Removal, Unlawful Presence or Illegal Reentry**. (g) **Miscellaneous Conduct**.

**You may** render the topics so the user knows what is asked, and help organize the certified records a
disclosure needs — arrest report, charging document, plea agreement, final disposition, proof of completed
probation, any vacating order (traffic matters are excluded unless the fine was $500 or more, criminal
charges resulted, or alcohol, drugs or injury was involved). **You must never** suggest an answer,
characterize conduct, opine on whether something "counts", or draft an explanation of an adverse fact. **Any
Yes — or any No the user is unsure of — stops the workflow and goes to a licensed attorney before anything
is filed.** Say why: it shifts the standard of proof, it is an enumerated reason to require an interview,
and a wrong answer creates the very misrepresentation ground the form asks about, under penalty of perjury.

## Part 2 → Part 3 — the affidavit-of-support decision (a closed rule)

An I-864 is required in an employment-based case only if **all three** hold: (1) the I-140 petitioner is the
applicant's — or, for a derivative, the principal's — relative, or that relative holds a significant
ownership interest (5% or more) in the petitioning business; (2) that relative is a spouse, parent, child,
adult son or daughter, or sibling; (3) that relative is a U.S. citizen, U.S. national, or LPR. All three →
the I-864 is required, Part 3 takes the "required" option, failing to file it is a denial, and that pattern
is outside this skill, so stop. Otherwise Part 3 takes the option meaning no exemption applies — where
self-petitioners land trivially.

## Supplement J vs the self-petitioner statement

- **Employer-petitioned I-140** (EB-1B, EB-2 PERM, EB-3) filed as a principal **after** I-140 approval →
  **Supplement J required**, signed by applicant and employer, photo ID copy behind it.
- **Filing concurrently with the I-140, or while it is pending** → no Supplement J, any category. And
  **self-petition categories — national interest waiver and extraordinary ability — never file Supplement
  J**, at filing or later: those categories are not tied to a specific job offer.
- **What a self-petitioner files instead**: a short signed and dated statement confirming they intend to
  work in the occupational field specified in the I-140 — and not even that when filing at the same time as,
  or while, the I-140 is pending. Draft it from the applicant's own facts: one page, first person; an
  opening declaration of intent to continue in that specific field; three or four sentences of training,
  relevant experience and principal accomplishments; then four or five sentences on two or three concrete
  projects or goals in the field and how they will be pursued in the U.S. Its legal job is narrow —
  continuing intent in the same field — so it must not re-argue the I-140 merits.

## I-765 and I-131 — the facts, and where the choice stops

Filing and holding them is harmless; **using** either is a hard stop. What follows is a fact table,
not a decision tree: give the user the mechanics so they can decide whether to FILE, and
characterize nothing about their status for them.

**EAD, Form I-765, category (c)(9).** Approval is independent of priority-date currency. A **pending
I-765 confers no work authorization** — if status-based authorization lapses before the card arrives,
the applicant must stop working. Re-entering on advance parole ends status-based work authorization.
Whether the user's own status already authorizes the work they need, and until when, is for the user
or counsel to state — do not answer it for them.

**Advance parole, Form I-131, the "pending I-485" application type.**
- **Departure while the I-485 is pending, without advance parole, abandons the I-485** — 8 CFR
  245.2(a)(4)(ii)(A). There is no appeal from the resulting denial.
- 8 CFR 245.2(a)(4)(ii)(C) carves out a narrow exception. Its conditions, quoted as the regulation's
  text and **not** as a finding about this user: the applicant is in lawful **H-1 or L-1** status
  and, on return, (1) **remains eligible** for H or L status, (2) **is coming to resume employment
  with the same employer** for whom previously authorized as an H-1 or L-1, and (3) **is in
  possession of a valid H or L visa** if one is required. H-4/L-2 dependents are covered on the same
  terms minus the same-employer condition, provided the principal is maintaining H-1/L-1 status;
  K-3/K-4 and V have parallel carve-outs. **All the conditions must hold — a valid visa foil by
  itself is not the exception**, and a change of employer or a status that can no longer be
  maintained takes the traveller outside it.
- **Advance parole must be approved and physically in hand before departure.** A pending I-131 is not
  travel authorization, and **departing while it is pending kills that application**.
- It is not now-or-never: an I-131 may be filed later against a pending I-485 by attaching a copy of
  the I-485 receipt notice. But processing runs months — read the posted I-131 time at
  egov.uscis.gov/processing-times when the question arises — and no travel is possible until the
  document is in hand, so an unplanned trip cannot be accommodated quickly.
- The document does not entitle anyone to be paroled: CBP decides afresh at the port of entry.

**Hard stop — the use fork.** Whether this user fits the (a)(4)(ii)(C) exception, and whether to
re-enter on advance parole or on the H/L stamp, is attorney territory (SKILL.md #12). State the
trade-off neutrally — parole is **not** an admission and ends the underlying nonimmigrant status,
re-entry in H or L preserves it, and that status is the only thing standing between an I-485 denial
and a Notice to Appear — then refuse the recommendation and refer to counsel. Whether to use the EAD
to work is the same stop.

Both forms: filing them together often yields one **combo card**, which serves as advance parole only
if it carries the advance-parole legend near the bottom — without it the card is an EAD and does not
authorize re-entry. I-765 eligibility category is **(c)(9)**; items keyed to other categories stay
blank, and the usual I-94/passport documentary requirement does not apply (photo ID and photos still
do). On the I-131 select **only** the pending-I-485 type — a different type chosen to unlock online
filing is punished with denial and no refund.

## The employment verification letter (principal only)

Employer's letterhead, addressed to the immigration officer, wet-ink signed by someone the employer
authorizes to sign employment letters, dated close to filing; submit the ink-signed original if possible.
Required content: the applicant's name; employer name and city/state; confirmation of **full-time**
employment; the **start date** (month and year at minimum); **current salary or wage with the pay basis**;
**current job title**; and a brief description of duties or research focus, the more substantive the better,
since it ties current work to the I-140 occupational field. **The omission that matters most: the letter
must NOT state an employment end date** — open-ended is materially better, because the I-485 turns on
*continuing* intent.

**PhD candidate on a stipend** — same format, different content: name and identification as a PhD candidate
in a named department at a named university with city and state; the date the enrolment or appointment
began; the stipend amount and its period; **two or three sentences of substantive detail on the research**,
carrying the load in place of a duties paragraph; and an offer of further information.

## Signatures

- USCIS will not accept a stamped or typewritten name in place of a signature, and **an unsigned form is
  rejected**. A photocopy, fax or scan of a document bearing a handwritten ink signature is acceptable for
  filing. Sign in black ink. A parent or legal guardian may sign for a child under 14, a legal guardian for
  a person adjudged mentally incompetent; any additional-information sheet with content must itself be
  signed and dated. The applicant re-affirms the contents under oath at biometrics, and re-signs at an
  interview if any answer is added or revised.
- On dating: there is **no published rule that an I-485 signature must be within N days of filing** — do not
  assert one. Keeping forms and time-sensitive letters fresh is a common practitioner convention, not a
  requirement; say which it is and let the user decide. Either way, do not assemble far ahead of filing.

Sources: Form I-485 and Instructions 01/20/25; Forms I-765, I-131, I-693 and I-485 Supplement J with their
instructions; uscis.gov "Tips for Filing Forms by Mail"; USCIS Policy Manual Vol. 7 Pt. A Ch. 5, 10, 11 and
Pt. E Ch. 5; Form I-864 Instructions (EB trigger rule); FR doc 2026-14539 (public charge, eff. 2026-09-18).
Checked 2026-08-04 — re-verify every edition date at fill time.
