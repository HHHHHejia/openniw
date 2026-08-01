# NIW Petition Document Structure (de-identified analysis)

Derived from structural analysis of a real, professionally-prepared NIW filing.
All personal identifiers replaced with placeholders. This document drives the
drafting-engine templates in `backend/app/prompts/`.

## Petition Letter (PL) — canonical outline

- Front matter: date, USCIS lockbox address, RE block (Petitioner/Beneficiary,
  Type: I-140, Classification: INA §203(b)(2)(B) National Interest Waiver),
  opening paragraph invoking Matter of Dhanasar, a./b./c./d. roadmap list.
- Auto TOC.
- I. Advanced degree (1 paragraph, 2 sentences; cites diploma exhibit).
- II. Prong 1 — substantial merit and national importance (~1,850 words).
- III. Prong 2 — well positioned (~2,000 words, heaviest quantitative section).
- IV. Prong 3 — on balance (~840 words).
- INDEX OF EXHIBITS, three groups: Academic and Professional Background (1–3),
  Publications and Citations (4–18), Other (19–33).

Target total: ~5,200 words / 14–15 pages. No sub-headings inside sections;
segmentation via topic sentences and bullet lists.

### The canonical endeavor sentence

A single ~90-word endeavor sentence is composed once and repeated VERBATIM at
~10 fixed slots (TOC, headings, section openers/closers). Slots:

> "developing and applying [METHOD-1], [METHOD-2], and [METHOD-3] to build
> [QUALITY-ADJECTIVES] [TARGET-SYSTEM] systems capable of [CAPABILITY-1..3]
> in order to [NATIONAL-BENEFIT-1..3] across critical domains such as
> [DOMAIN-1..3] in the U.S."

### Section II module stack (each paragraph = one module, one anchor exhibit)

1. Endeavor declaration (cites PES exhibit)
2. International/policy alignment (UN/IGO documents)
3. Concrete projects + federal standards alignment (e.g. NIST framework, DOE targets)
4. National economy / market size (market report + macroeconomic projection)
5. Employer-independence argument (no exhibit)
6. Federal R&D budget priorities (OMB/OSTP memo)
7. Critical & Emerging Technologies list mapping (NSTC CET list)
8. Open-source / public-good contribution (repo metrics)
9. Federal research funding (grant pages + agency mission page)
10. USCIS Policy Manual national-importance restatement (footnote authority)
11. One-sentence close ("enduring national significance")

### Section III module stack

1. Dhanasar Prong-2 framing sentence + footnote with the multifactor test
2. Education + employment + future plan (contains the waiver disclaimer:
   "This petition waives the job offer requirement, and the petitioner's
   proposed endeavor is separate from his proposed employment...")
3. Peer review service (count + venue prestige rankings)
4. Research contribution bullets (3–5, gerund-initial, problem → method → result)
5. Publication tally by type × authorship role + venue-ranking bullets
   ("[VENUE]: Ranked #N in [CATEGORY] by Google Scholar.")
6. Total citations + per-paper citation-percentile bullets:
   "[APPLICANT]'s article, '[TITLE],' published in [YEAR] in [VENUE], has
   received [C] citations to date. For all articles published in the category
   of [ESI-CATEGORY] in [YEAR], the average number of citations is only [AVG].
   This article is thus one of the top [P]% most cited articles..."
7. Citation-percentile methodology defense (bibliometrics authority exhibit)
8. Independent citing-work bullets (3): "In a [YEAR] study in [VENUE],
   [AUTHOR] et al. employed/incorporated/built upon [APPLICANT]'s work to
   [WHAT], showing [RESULT]. This citation highlights/emphasizes/illustrates..."
9. Award module with computed selectivity ratio
10. Section close: single long sentence restating the endeavor verbatim

### Section IV module stack

1. Recap (degree + expertise + record; endeavor not tied to a position)
2. Value-to-U.S. restatement; "benefits outweigh the interests served by the
   labor certification process"
3. Urgency (pressing national challenges recognized by agencies)
4. Bridge sentence
5. Impracticality of labor certification (delays inconsistent with a dynamic field)
6. Minimum-requirements argument (labor cert assesses minimums; cannot capture
   unique expertise exceeding them)
7. Conclusion: "clearly satisfies the third prong"

### Citation & exhibit conventions

- Inline `(Exhibit N)`, ranges with en-dash `(Exhibits N–M)`, sentence-final.
- Sub-letters a/b pair "applicant-specific proof" + "legitimizing context".
- Legal authorities (Dhanasar, Policy Manual) cited in FOOTNOTES only.
- Exhibit numbering is positional within three fixed groups.
- Field-generic exhibits (policy corpus, legal authorities, bibliometrics
  methodology) form a reusable per-field library — not user-supplied.

## Proposed Endeavor Statement (PES)

First-person signed declaration, filed as an exhibit, ~1,300 words / 4 pages.
Own reference system `(Reference N)` + "List of References" (subset of PL exhibits).

Outline:
1. Endeavor declaration ("My proposed endeavor is to ...", same canonical sentence)
2. National-interest alignment (three "policy hook → my contribution" pairs)
3. Planned research topics — 3 bullets, each rigidly 5-part:
   (a) gerund title, (b) goal, (c) U.S. beneficiaries/benefit,
   (d) explicit endeavor-linkage sentence, (e) timeline + institution
   (past tense if started, future if planned)
4. Employment as vehicle + employer-independence caveat (load-bearing legal
   argument, stated twice — opening and closing)
5. Role description at current employer (title, start, salary, benefits)
6. National significance of employer's work
7. Secondary affiliation (if any)
8. Closing re-emphasis + dissemination plan
Signature block (date + "do not sign until instructed" hold).

## Evidence corpus conventions

- One node per exhibit: `<N>.pdf` | `<N>_<label>.pdf` | `<N><letter>.pdf` |
  `<N>/` directory | `Additional file for ex<N>[_k].pdf`.
- Peer-review evidence: per-venue folders with complete email trails
  (conference: invitation → acceptance → assignment → review-received;
  journal: invitation → decision → thank-you → review report).
- Publication supplements: acceptance emails, OpenReview pages.
- Awards: nomination email + public award listing + screenshot.
- Funding: award-abstract pages + agency mission page.

## Derived quantities the generator must compute

- Publication tallies by venue_type × authorship_role
- Citation-percentile tier per paper (needs ESI-style yearly averages)
- Percentile tier tallies across papers
- Award selectivity = n_selected / n_total_submissions
- Peer review total count
- Exhibit numbers (positional, after ordering)

## Fixed/variable ratio

~55–60% of the PL is field-generic boilerplate; ~40–45% applicant-specific.
The PES is ~50/50. Lint rules worth automating: honorific consistency,
prong-numbering convention, no dangling template instructions, no truncated
names, endeavor sentence repeated verbatim (never paraphrased).
