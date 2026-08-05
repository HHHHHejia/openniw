# Stage II·a — History Assembly

The organising principle, and the reason this stage exists: **the record must run
continuously from first U.S. entry to today, for the principal and for every
derivative, with no unexplained gap.** Every segment resolves to either a document
or a signed written explanation. This is the highest-value clerical work in the
whole workflow and the one an agent does better than a person with a shoebox.

Four files, built in this order. Write each one incrementally — never wait until
a file is "complete" to save it.

## The loop discipline

Ask for **one item at a time**. Name the exact document, say where it usually
lives, and say what you will do with it. Upload waves go through
`openniw ui intake` and land in `sources/`. After each item: write it into the
right history file, update case.json if it carries an identity fact, update
STATE.md, then ask for the next one. A wall of twenty questions produces four
answers; a single question produces one answer every time.

When a document arrives, read it and extract rather than asking the user to
retype. When two documents disagree, surface both and ask once.

## history/status-history.md

One row per status interval, oldest first:

`from | to | status/class | I-94 number | document that proves it | in sources/?`

The proving document by status:

| Status held | Required |
|---|---|
| F-1/F-2 | **every page of every I-20 ever issued**, all versions |
| OPT / STEM OPT | front **and** back colour copies of **every** EAD ever held, filed with the I-20s |
| J-1/J-2 | **every page of every DS-2019 ever issued** — plus the full 212(e) branch in `eligibility.md` |
| J-2 with an EAD | front and back of those EAD cards, with the DS-2019s |
| H, L, O, TN, E and other petition-based | **every** I-797 approval notice ever issued, including for extensions and amendments |
| Any status | the I-94 record covering it |
| Parole | the parole document and the I-94 showing parole |

Plus, once: the passport biographic page and **every** U.S. visa stamp, entry
stamp and immigration endorsement in every passport including expired ones.

**I-94 mechanics that trip people up** (get these right or three forms disagree):
- Retrieve electronic records at the CBP I-94 site; entries before April 2013 are
  paper cards in the passport. If a record is missing, Form I-102 exists.
- The I-94 number is usually 11 digits. After an approved change or extension of
  status a new I-94 appears at the **bottom** of the I-797 approval notice, but
  the number itself usually stays the same.
- **Authorized-stay expiry comes from the I-94 record** — the "VALID FROM … UNTIL"
  block at the bottom of the I-797 — **not** the date printed at the upper right
  beside the status class. Those two can differ; the I-94 date governs. F and J
  usually read `D/S`.
- The **passport used at the last entry** is the one that must match the I-94,
  even if it has since expired. A newly renewed but unused passport is the wrong
  answer.
- **Status at last entry** and **current status** are different questions and are
  routinely conflated (entered F-1, now H-1B → last entry was F-1). If the last
  entry was on advance parole, the status at entry is parole.
- Place of last entry needs city **and** state, or city **and** country — never a
  city alone. A land entry from Canada with no electronic I-94 is still reported.
- Dates are mm/dd/yyyy everywhere. Flag this early for applicants from dd/mm
  countries and re-check every date they give you.
- An error on the I-94 record is worth raising with the DSO or responsible officer
  — but **do not hold the filing waiting for a correction**.

## When a document cannot be produced

Every missing document becomes a **signed written explanation** that you draft
from the user's own facts and they sign and date. Required content:

- **Missing status document (I-20, DS-2019, I-797, EAD):** which form is missing,
  its validity dates, the sponsoring school or employer, why it is missing, and a
  statement that the applicant asked that school or employer for a copy and it was
  not available.
- **Lost or surrendered old passport with U.S. stamps:** the visa type(s) it
  carried, their validity dates, the issuing consulate or embassy, and why the
  passport is gone.
- **No port-of-entry stamp at all:** date of last entry, mode of transport, port
  of entry, and an affirmative statement that no I-94 record or stamp was issued.
- **Last entry through Canada with no I-94 record:** use the Canadian-border entry
  date as the date of last entry on **every** form, and submit the most recent
  I-94 record together with the port-of-entry stamp.

Draft these in the applicant's own voice, short, factual, first person, no
argument and no characterization. They file **behind the exhibit they explain**,
not in the cover letter.

If the user describes a period with **no lawful status at all** — rather than a
missing piece of paper — that is a hard stop, not an explanation letter. Say so
and stop that thread.

## history/addresses.md

Every physical address for the **last five years**, most recent first, with
move-in and move-out month/year and no gaps between them. Plus the current U.S.
physical address with the date the applicant first lived there, the mailing
address if different, and the most recent address **outside** the U.S. where they
lived for more than one year.

Rules: physical addresses, not P.O. boxes. A sublet, a friend's couch, or a
university dorm is still an address and is still listed. Any month unaccounted
for gets chased, not skipped.

Note the standing duty now so it lands in `timeline.md` later: USCIS must be
notified of any move within **10 days**, for the entire pendency and beyond.

## history/employment.md

**All employment AND education for the last five years**, most recent first,
including self-employment, unemployment and retirement. Per entry: employer or
school name, full address, job title or program, and start/end month and year.

Every non-working period needs its **source of financial support** stated — this
is an explicit form requirement, not an optional nicety, and it is where personal
savings, a spouse's income, a stipend, or family support belong.

Also capture: the most recent employer or school **outside** the U.S., whatever
its date; and, for the principal only, the facts the employment verification
letter will need (see `forms.md`) — employer legal name and location, full-time
status, start date, current salary and pay basis, job title, and a short duties
or research description.

If the principal is unemployed at filing, flag two distinct requirements that both
apply: evidence of self-support, **and** evidence of continued engagement in the
same occupational field as the I-140. Collection for the second starts now and
continues after filing, because that RFE, if it comes, arrives months later and
asks about the interim period.

## history/travel.md

Every departure and return since first entry, with dates, destination, and the
document used to re-enter. This feeds three later steps: 212(e) physical-presence
proof if it applies, the manner-of-last-entry answer on the I-485, and advance
parole planning. It is also the record that will show, when you build it, whether
the continuous status story actually holds together.

## Finishing the stage

The stage is done when: every interval from first entry to today has a document or
a signed explanation; addresses cover five years with no gap; employment and
education cover five years with support stated for every non-working month; travel
is complete; and every derivative has their own four files, name-prefixed
(`history/spouse-status-history.md` and so on). Record the count of open gaps in
STATE.md, not a vague "mostly done".

Sources: Form I-485 Instructions 01/20/25 (Parts 1, 4 — the biographic collection
that replaced Form G-325A); uscis.gov/i-485Checklist; CBP I-94 retrieval site;
8 CFR 103.2(b) (evidence and secondary evidence). Checked 2026-08-04.
