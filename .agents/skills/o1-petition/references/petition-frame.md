# Stage II·a — The Petition Frame (the user and petitioner choose; then fixed)

An O-1 stands on four framing decisions. **None of them is yours to make.**
The petitioner structure in particular is a legal and commercial choice
belonging to the beneficiary AND the actual petitioning entity: analyse the
factual fit, documentation burden and unresolved issues of each structure,
present the comparison, and ask them to select and confirm. Never label one
"recommended", "best" or "selected" — mark unavailable structures as such
where a fact rules them out, and say when the information is too thin to
compare. Record all four in `petition-frame.md`, dated, before Stage II·b: every document repeats the
field label VERBATIM, the evidence checklist depends on the petitioner
structure, and post-filing changes to petitioner, role, or terms are
material changes requiring an amended petition (8 CFR 214.2(o)(2)(iv)(D)).

## 1. Petitioner structure (decision tree)

Self-petition is prohibited ("An O alien may not petition for himself or
herself" — 8 CFR 214.2(o)(2)(i)). One beneficiary per petition. Pick one:

**A. Direct U.S. employer** (the default when a real job offer exists).
Evidence: signed offer letter or employment agreement (title, duties,
wage, start/end dates) — or, if terms are informal, the regulation's
**summary of the oral agreement** (terms offered + terms accepted; need
not be signed by both parties); employer's basic corporate facts for the
I-129. The employer signs the I-129 and the support letter. Concurrent
jobs: each employer files its own petition unless an established agent
files one.

**B. U.S. agent** — for the traditionally self-employed, multi-employer
arrangements, or a foreign employer with no U.S. entity. The agent can be
(i) the actual employer, (ii) a representative of both employers and
beneficiary, or (iii) an entity authorized by the employer(s) to act as
agent. Evidence by sub-type (8 CFR 214.2(o)(2)(iv)(E)):
- agent-as-employer: the contractual agreement between agent and
  beneficiary specifying wage and terms;
- agent for multiple employers: a **complete itinerary** (dates of each
  engagement; names AND addresses of each actual employer; names AND
  addresses of each venue/location), **contracts between each employer
  and the beneficiary**, and a signed authorization statement from each
  employer that the agent may file on its behalf (compensation of the
  agent is not required; without established authority USCIS limits
  validity to the agent's own engagements);
- foreign employer via U.S. agent: agent accepts service of process; the
  foreign employer stays liable for employer-sanctions compliance.
Warn the user: the itinerary is a cage, not gig-economy freedom — work
for an employer not on it is unauthorized; speculative or contingent
engagements cannot be listed; a named employer folding auto-revokes the
approval; a new company founded later needs an amended petition BEFORE
work begins.

**C. Beneficiary-owned entity** (founders). The Policy Manual (Vol. 2
Part M Ch. 3, since the 2025-01-08 policy alert): "a separate legal
entity owned by the beneficiary, such as a corporation or limited
liability company, may file the petition on their behalf" — majority
ownership included. Evidence package: certificate of incorporation
(practitioners favor a C-corp over a single-member LLC); a signed
employment agreement (title, duties, salary) as the required contract;
board with at least one independent member and documented authority to
supervise, evaluate, compensate, and terminate the founder; board
minutes/consents showing real oversight; cap table + investor documents
(SAFEs/priced round) showing outside stakeholders; payroll records;
company traction. Drafting checklist question (conservative practice,
not a regulation): "could this founder be fired on paper?" Anti-patterns
that draw scrutiny: patents filed only for the petition, advisory boards
invented for immigration, paid press, everything dated weeks before
filing, evidence that is entirely self-generated.

Record the choice, the signatory (name + title), and the entity facts in
case.json (standing rule 2).

## 2. Field of extraordinary ability (the frozen label)

One phrase, e.g. "machine learning for computational biology" — narrow
enough that the beneficiary is credibly at the very top of it, broad
enough that the U.S. role sits inside it. The "area of extraordinary
ability" is read broadly (related occupations sharing skillsets:
researcher → industry scientist, engineer → founder), but every duty of
the proposed role must map onto the acclaimed specialty —
acclaim-as-researcher + role-as-generic-PM is a classic RFE. Once frozen,
the label appears verbatim in the support letter, consultation, expert
letters, and I-129.

## 3. Role + itinerary scope (the #1 RFE trap)

Mandatory initial evidence (8 CFR 214.2(o)(2)(ii)): an explanation of the
nature of the event(s) or activities, their beginning and ending dates,
and a copy of any itinerary. "Event" is generous — a scientific project,
business project, academic year, engagement, or an ongoing job can be the
event, and related activities with gaps still count — but **speculative
employment or freelancing is not allowed**: concrete events/contracts must
cover the whole period requested. Freeze:
- role title + duties (each mapped to the field label);
- the event/activity description with start and end dates;
- work locations; for agent/multi-employer cases the full per-engagement
  itinerary table (employer legal name + address, venue + address, dates,
  rate, supervisor);
- requested validity: up to 3 years — request the full period the
  documented events support. Extension math for later: same event renews
  in ≤1-year increments; a NEW event (a different phase or trial of the
  same research counts) supports a fresh up-to-3-year grant; unlimited
  extensions.

## 4. Consultation plan

A written advisory opinion is mandatory initial evidence (8 CFR
214.2(o)(5)). Decide now who signs:
- **Listed peer group or labor organization** where one exists (USCIS
  publishes an "Address Index for I-129 O and P Consultation Letters";
  mostly arts/athletics bodies, some business/CS-adjacent — check it; some
  charge fees and take weeks). A "no objection" letter suffices.
- **Individual expert(s)** — the regulation's peer group "could include a
  person or persons with expertise in the field", the standard route for
  sciences/CS/engineering where no union or standing peer group exists.
  The letter states that no appropriate peer group or labor organization
  exists for the field, then gives the opinion. Signer hygiene: recognized
  expert in the field or an allied one, ideally with substantial U.S.
  history, and NO conflict of interest — never an investor, advisor, or
  employee of the petitioner. Consultation ≠ recommendation letter; the
  same person should not sign both.
- **No-peer-group route**: if the petitioner establishes none exists,
  USCIS decides on the record — still write the no-peer-group statement.
- If a non-labor-org opinion is filed and a union DOES exist for the
  occupation, USCIS forwards the petition to it for a 15-day comment
  window — one more reason to state explicitly that no union covers the
  field. O-1B MPTV is different: BOTH the union and a management
  organization must be consulted, and comparable evidence is barred.
- If the consulting entity issues watermarked letters, file the
  watermarked version (authenticity RFEs otherwise).

## Record in petition-frame.md

```markdown
# Petition Frame (confirmed 2026-08-02 — changes require re-confirmation + impact check)
## Petitioner (user-and-petitioner-confirmed structure): [A/B/C] — [legal name], signatory [name, title]
   evidence needed: [...]                    status: [...]
## Field of extraordinary ability: "[frozen label]"
## Role & event: [title] at [org], [start]–[end] — [event description]
   itinerary: [inline table or "single site: address"]
   requested validity: [dates, ≤3 years]
## Consultation: [signer/org], route [peer group | expert + no-peer-group | on-record]
   conflict check: [clean/issue]             status: [requested/received]
```

Record only what the user AND the actual petitioner have both confirmed —
the structure field is headed `user-and-petitioner-confirmed`, never
`recommended` or `agent-selected`. Date it and log it in STATE.md. After
confirmation the frame is fixed; post-filing changes to petitioner, role or
terms are material changes requiring an amended petition.

Sources: 8 CFR 214.2(o)(2), (o)(5) (eCFR); USCIS Policy Manual Vol. 2
Part M Ch. 3, 7, 9 (uscis.gov/policy-manual); policy alert 2025-01-08
(beneficiary-owned entities); practitioner practice: deel.com,
compassvisas.com, tryalma.com, porticovisa.com (conservative view).
