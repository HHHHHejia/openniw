# Law-Firm NIW Process Reconstruction (de-identified analysis)

Derived from a top NIW firm's client packet and portal. Drives OpenNIW's user
flow, intake design, and content patterns. No personal information.

## The pipeline (firm's 10 steps → OpenNIW's 5 stages)

1. Provide CV, degree documents, Google Scholar URL
2. Fill four tabs: Proposed Employment/Proposed Endeavor (PE/PE), Research
   Background Inquiry Form (RBIF), Publication Record, Recommenders
3. Preliminary Proposed Endeavor Statement draft (1–3 business days) → client
   revises via track changes
4. Petition Letter + support letters first drafts (10–15 business days)
5. Revision cycles (1–3 days each)
6. Questionnaire tab + ETA-9089 tab (form generators — client NEVER fills a
   blank I-140/G-28/ETA-9089; the system generates PDFs from tab data)
7. Collect signed support letters (hand/verified signature only, letterhead
   preferred; check signers didn't change letters "in harmful ways")
8. Finalize PL + PES; client signs; forms issued & signed
9. Upload exhibits (only AFTER the petition letter is finalized — its Exhibit
   Index is the shopping list)
10. Final QC, print, FedEx to lockbox; receipt notice 7–30 days

## Free evaluation intake (the complete field set)

Part 1 Basics: salutation+name, country of birth, email, phone, petition
category (NIW/EB-1A/EB-1B/O-1A/"not sure — recommend"), current visa status.
Part 2 Background: field of study; repeating degree group (type, major,
university, year, "is this degree related to your proposed endeavor?" per
degree); currently employed + position; citation profile URL; citation count;
publication count (peer-reviewed only); year of most recent paper; papers
reviewed (+ evidence self-certification checkbox); patents Y/N; funding Y/N.
Part 3 Continuity: still researching/publishing?; planned work aligned with
prior education/publications?
Part 4: CV upload (required), attribution channel, authenticity declaration.
Promise: personalized response within 24 business hours.

## The endeavor sentence composer (best UX pattern in the corpus)

Three questions, each ≤50 words:
A1 method/approach (active verb, ≤3 primary methods)
A2 specific topic/focus
A3 intended impact ("in order to ..." clause)
→ mechanically concatenated: "My proposed endeavor is to [A1] [A2] in order to
[A3]." → then reviewed/polished. Plus: how employment supports it (1–3
sentences); why important to the U.S. (2–4 sentences, link government strategy
docs); 2–3 FUTURE projects (not completed ones), each: title, start date, goal
+impact, endeavor linkage, where/with whom, government funding if any;
publication plans (venues, in-prep manuscripts, 6–12 month timeline).

Adjudication-trend note the firm gives clients: academic/research-framed
endeavors face less Prong-1 scrutiny than industry-framed ones; frame industry
work by its research value and national alignment (without misrepresenting).

## RBIF (drives the petition letter body)

Main field (not too broad, not too narrow, interdisciplinary bridge if
transitioning) · up to 3 CET categories/specializations · importance of the
endeavor (problem/impact/broader-relevance scaffold, plain language, cite
national strategies, emphasize U.S. work) · up to 3 key publications, each as
sentence stems: "In [citation]" → "I described [~100 words: problem →
methodology → results]" → "advances my proposed endeavor by [50–100 words]" ·
up to 3 examples of others using the work (same stems on the citing paper) ·
supplementary: funding (US-based, external), awards (external, competitive; NO
student awards), media (name must appear; no employer press releases), peer
review (venue+count+formal invitation?), commercialization/patents (granted
only), leadership roles, open-source (name+links, role, adoption metrics,
U.S. relevance, recognition), memberships (selective only; senior/fellow
valued), high salary (top 10%).

## Support letters (current doctrine)

Max 4 letters total ("fewer is often better — too many distract from objective
evidence"). Ranked effectiveness:
1. National Importance TL from U.S. governmental/quasi-governmental entities
   (quasi-gov includes state universities, USPS, transit authorities)
2. Planned Research TL from employers/supervisors/advisors/collaborators/
   funding-org representatives
3. Recommendation letters on completed research — dependent preferred; for
   independent, prefer people who cited the work
Signers: established professionals (no students/postdocs), familiarity >
title, ≥half U.S.-based, different states ideally. Letters must avoid:
speculative language (potential/possible/may/probably), qualifying language
(young researcher/early career/rising star), and the signer's own
citation/publication counts.

TL anatomy (National Importance): credentials → relationship → thesis → lay
explanation of research + joint project → funding-as-endorsement paragraph →
national statistics + consequence chain → conclusion naming 3 specific
technical competencies → recommendation.
TL anatomy (Planned Research/combined): capacity + relationship + endeavor
restated + "Please accept this letter as verification of..." → project
paragraph (what/builds-on/supports-endeavor/where/funding/national issues) →
national-issue paragraph (gap → harm → what the work introduces → second-order
benefits) → conclusion.

## Evidence rules (encode into checklist ai_notes)

- Objective vs subjective: every subjective claim (letters) must be shadowed by
  an objective exhibit. Build the exhibit index FROM the claims.
- Publications: first 3 pages per exhibit-worthy article, name highlighted;
  venue+year visible. Books: cover + TOC + © page + first 3 pages.
- Citation report: Google Scholar ONLY (multiple databases confuse officers and
  invite RFEs). Printed to PDF from the site.
- Notable citations: first page + every page citing the work (highlighted) +
  references page (client's paper highlighted). Published articles only.
- Peer review: editor thank-you emails or "reviews completed" page; Publons
  alone no longer accepted; revised-manuscript reviews count separately only
  with clear evidence of two rounds.
- Awards: include selection criteria (how many given, out of how many).
- Degrees (NIW): diploma + official transcript + NACES general evaluation for
  foreign degrees. Registrar-letter alternative (4 data points).
- Media: applicant must be named; employer/university press releases excluded.
- Funding: grant docs naming the person, or acknowledgment sections of papers.
- Translations: certified; no machine translation; translation as separate
  page; name affidavit for name variants; don't sign affidavits until the PL
  is final.
- Screenshots must show the full URL. Highlight the applicant's name in author
  lists. Webpage captures logged-out.

## Forms guidance (encode into wizard help text)

- I-140 Part 2 for NIW = box 1.h (this maps to checkbox state /h). Part 5 =
  Self. Occupation ≠ job title (reflects overall work/research). Annual income
  = salary + cash bonus only. Nontechnical job description <200 chars, no
  employer/project/region names, research duties emphasized, NO teaching
  duties (officers don't view teaching as nationally important).
- Processing: if unsure between adjustment and consular, check consular ("more
  difficult to change to IVP later than the reverse"). India/China-born
  usually cannot file I-485 concurrently (retrogression).
- SOC code is what USCIS uses at I-485 stage to check "same or similar field".
- ETA-9089 education: highest U.S. advanced degree relevant to the endeavor,
  or evaluated foreign equivalent. Training section: usually N/A ("unnecessary
  information may attract additional scrutiny"). Job duties: 3–5 sentences,
  action verbs, no job title/employer/advisor/grant names. Flag overlapping
  work-experience dates.
- Fees (self-petition): I-140 $715 + Asylum Program Fee $300 = $1,015; premium
  (I-907) $2,965. One payment method per filing; premium fee needs its own
  form; declined card = whole package rejected (prefer ACH).
- Signatures in black ink; no typed signatures; print single-sided; no staples.

## Content/UX patterns to reproduce

- Instruction triplet on every field: "Instructions / Why we ask / What to
  include" (+ Examples). The "why" ties the field to a downstream document or
  a Dhanasar prong.
- Explicit word budgets everywhere (≤50 words, 2–4 sentences, max 3 items).
- Negative constraints listed as thoroughly as positive ones.
- Ranked-preference lists with reasoning, not binaries.
- Deliberate omission as strategy ("unnecessary information attracts scrutiny").
- Idle-time parallelization: collect evidence while waiting on drafts.
- Named SLAs at every handoff; message-on-every-upload protocol.
- Statistic → bridge → claim pattern for national-importance paragraphs.
- The portability disclaimer in every PES.
- Provenance tags on all guidance: statute vs USCIS policy vs firm heuristic.
