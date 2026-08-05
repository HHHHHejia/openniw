# OpenNIW — NIW · EB-1A · O-1 · I-485

**Free, open-source agent skills that help you organize and speed up your
own U.S. immigration paperwork — the EB-2 NIW and EB-1A self-petitions, the
O-1A petition kit, and the employment-based I-485 that follows. Your coding
agent does the organizing, a local folder is the case file, and a browser
wizard appears exactly when a GUI beats chat.**

## Star History

<a href="https://www.star-history.com/?type=date&repos=HHHHHejia%2Fopenniw">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=HHHHHejia/openniw&type=date&theme=dark&legend=top-left&sealed_token=LM_nSQf175i0EfYyrAMhEuCJKFbbUAaocH7IoAZkHAxLZsJKZsEUT5jhWB0gDxHpvmgMvGA0UQJOxMtD109gKhJwWKXLoZC0Rvo6cM6JA9Uw-pw9m3g4fQ" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=HHHHHejia/openniw&type=date&legend=top-left&sealed_token=LM_nSQf175i0EfYyrAMhEuCJKFbbUAaocH7IoAZkHAxLZsJKZsEUT5jhWB0gDxHpvmgMvGA0UQJOxMtD109gKhJwWKXLoZC0Rvo6cM6JA9Uw-pw9m3g4fQ" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=HHHHHejia/openniw&type=date&legend=top-left&sealed_token=LM_nSQf175i0EfYyrAMhEuCJKFbbUAaocH7IoAZkHAxLZsJKZsEUT5jhWB0gDxHpvmgMvGA0UQJOxMtD109gKhJwWKXLoZC0Rvo6cM6JA9Uw-pw9m3g4fQ" />
 </picture>
</a>

Website: **[openniw.com](https://openniw.com)** — project intro, install
guide, and a free no-signup statistical evaluation against 7,458 approved cases
(fully static; source in [webpage/](webpage/)).

OpenNIW ships four [Agent Skills](https://agentskills.io) —
`niw-petition`, `eb1a-petition`, `o1-petition`, and `i485-adjustment`.
Install them into
Claude Code, Codex, Cursor, or any Agent-Skills tool, and your existing AI
subscription runs the entire preparation workflow — evaluation, evidence,
drafting, official forms, filing package — with **zero configuration**:

- **No account.** Nothing to sign up for.
- **No database.** Your case lives in a local case folder you own.
- **No API key.** Your agent's subscription is the AI.
- **No server.** A localhost companion opens only when you reach a
  form-heavy step, and only talks to your case folder.

> **OpenNIW is a document-preparation and self-help tool, not a law firm, and
> does not provide legal advice.** Immigration outcomes depend on individual
> facts and adjudicator discretion. Review everything before filing; consider
> consulting a licensed attorney.

## Install

```bash
# cross-agent installer (Claude Code, Codex, Cursor, 70+ agents) —
# offers all four skills; install what you need:
npx skills add HHHHHejia/openniw

# or manually — Claude Code (swap in any of the four skill folders):
git clone https://github.com/HHHHHejia/openniw
mkdir -p ~/.claude/skills && cp -r openniw/.agents/skills/niw-petition ~/.claude/skills/

# or manually — Codex and other Agent-Skills tools:
mkdir -p ~/.agents/skills && cp -r openniw/.agents/skills/niw-petition ~/.agents/skills/
```

Then say **"帮我准备 NIW 申请"** or **"evaluate my NIW case"** in your
agent — or "evaluate my EB-1A case" / "prepare my O-1 petition" /
"help me file my I-485" for the sibling skills.

## The four skills

| Skill | Category | Status | What differs |
|---|---|---|---|
| `niw-petition` | EB-2 NIW self-petition (I-140 + ETA-9089 App. A) | shipped | Full flow incl. browser forms wizard, deterministic PDF fill, filing-package ZIP |
| `eb1a-petition` | EB-1A extraordinary ability self-petition (I-140, E11) | beta | All ten 8 CFR 204.5(h)(3) criteria, Kazarian two-step petition letter with Final Merits section, benchmark vs ~2,300 approved EB-1A cases; I-140 by field guide (wizard = roadmap) |
| `o1-petition` | O-1A petition kit (I-129; employer / agent / founder-owned entity) | beta | Petitioner-structure decision tree, consultation/advisory opinion, itinerary, signature-ready hand-off package for the petitioner; I-129 by field guide |
| `i485-adjustment` | Employment-based adjustment of status (I-485 on an approved or pending EB I-140) | beta | The step *after* the petition. Eligibility gating, status-history assembly, personalized document checklist, I-485 part-by-part guidance, package and post-filing timeline — **assembly only, see below** |

The beta skills were built from primary sources (USCIS Policy Manual, 8 CFR,
current fee schedules — all cited inline with as-of dates), open-source MIT
materials, and our 7,458-case approved-case dataset. They follow the same
frozen-frame doctrine, exhibit-bound drafting, and RFE red-team pass as the
NIW flagship. **If you have been through an EB-1A, O-1 or I-485 filing —
applicant or practitioner — we would love your review.**

### `i485-adjustment` is deliberately narrower — and here is why

The petition skills argue a case. The I-485 skill does not, because the
downside is different in kind: in 2026, USCIS is adjudicating adjustment as
a discretionary benefit, interviews are back for a meaningful share of
employment-based cases, vetting has expanded — and a denial for someone
with no other status can end in a Notice to Appear and removal proceedings.

So it is an **assembly and completeness tool**. It does the enormous
clerical burden: eligibility *gating* against published answers (I-140
basis, the Visa Bulletin chart USCIS designated this month, 212(e)),
reconstructing a continuous status/address/employment/travel history from
your first entry, the document checklist personalized by what actually
drives each requirement (including the birth-certificate substitute ladder
and country-specific documents), part-by-part form guidance for every
applicant in the family, package assembly, and the post-filing timeline.

And it **stops**, naming the fact that stopped it, on anything where being
wrong can hurt you: any answer in Form I-485 **Part 9** (the
inadmissibility block — renumbered from Part 8 in the 01/20/25 edition),
any criminal history at all, any overstay or unauthorized work, any
245(k)/245(c) day-count, misrepresentation, prior removal, unresolved
212(e), CSPA calculations, INA 204(j) "same or similar" determinations, and
the decision to actually *use* an EAD or advance parole (holding one is
harmless; using it ends your underlying nonimmigrant status). It will not
help you phrase around an adverse fact. Those refusals are the product, and
they are enforced by tests.

**Family-based I-485 is out of scope** (it needs Form I-864 and
sponsor-income analysis that is not implemented).

## How it works

```
        ┌──────────────────────────────────────┐
        │   Your agent + an OpenNIW skill      │   the BRAIN — conversation,
        │   (niw / eb1a / o1 / i485 · any agent)│   judgment, drafting, prefill
        └──────┬─────────────────────┬─────────┘
   reads/writes│                     │ launches at interaction-heavy steps
               ▼                     ▼
        ┌────────────┐   ┌───────────────────────────┐
        │ your case/ │◄──┤ openniw (pip companion)   │  the ORGAN — browser
        │ STATE.md   │   │ localhost form wizard +   │  wizard & deterministic
        │ case.json  │   │ citation review + PDF     │  compute; zero LLM,
        │ forms/ …   │   │ fill / package / harvest  │  zero keys, zero DB
        └────────────┘   └───────────────────────────┘
```

- Each **skill** drives every stage and survives weeks of short sessions:
  `STATE.md` in the case folder is read at every session start and updated
  after every step, so any session resumes exactly where the last one ended.
- The **companion** (`pip install openniw`, installed by your agent when
  first needed) serves a localhost-only, token-protected browser UI over
  your case folder for the steps where a GUI beats chat — reviewing 60+
  form fields, or picking your best ~10 citations from scored quote cards —
  plus headless deterministic commands the agent uses directly:

  ```
  openniw ui forms|citations   # browser session over the case folder
  openniw fill all             # fill I-140 / ETA-9089 App. A / Final Det. / G-1145
  openniw package              # filing-package ZIP in lockbox order
  openniw harvest "Title" …    # OpenAlex citing-paper harvest + screening
  openniw registry             # lint the claim→evidence table (see below)
  openniw fetch-forms          # download official blank PDFs
  openniw docx / highlight     # DOCX export · exhibit highlighting
  ```

  The browser session outlives your terminal: close everything, come back
  tomorrow, and the agent reconciles what you did from the session file.
  If the companion can't be installed (offline/sandboxed), the skill falls
  back to pure-stdlib scripts bundled with it — the GUI is an accelerator,
  never a requirement. Intake, benchmark, and citation pages work for all
  three categories; the forms wizard, PDF fill, and package ZIP are
  NIW-only today (EB-1A / O-1A run Stages IV–V as guided chat + field
  guides — wizard support is on the roadmap).

## The workflow, stage by stage

The three petition skills follow the same shape — six stages to filing, plus the
RFE-response stage if USCIS pushes back; each adapts to its law:

| Stage | NIW | EB-1A | O-1A |
|---|---|---|---|
| **I — Evaluate** | Tiered, Dhanasar prong-by-prong read | All ten 204.5(h)(3) criteria + Kazarian two-step test | 8 O-1A criteria + petitioner-feasibility read |
| **II·a — Frame** | FREEZE the canonical endeavor sentence | FREEZE field definition + target criteria + continue-work statement | FREEZE petitioner structure + field + role/itinerary + consultation plan |
| **II·b — Evidence** | Personalized checklist; citation pipeline (harvest → independence screen → full-text verify → browser portfolio pick) — shared by all three | ← same | ← same, plus contracts / deal memos / itinerary |
| **III — Draft** | PES → support letters → Dhanasar three-prong Petition Letter → exhibit index | Continue-work statement → letters → Kazarian two-step letter with Final Merits section | Petitioner support letter → consultation request → itinerary → expert letters |
| **IV — Forms** | Browser wizard over the 61-field answer set → deterministic I-140/ETA-9089 PDF fill | I-140 (E11) field-by-field guide | I-129 + O supplement field guide |
| **V — Package** | ZIP in lockbox order, state+premium-aware address | Assembly checklist, standard-vs-premium lockbox tables | Signature-ready hand-off kit for the petitioner |
| **R — RFE response** | Prong-by-prong diagnosis → evidence loop → government-letter line → supplemental PS → response package | Criterion-by-criterion + final-merits rebuttal → new-evidence loop → response package | Itinerary / consultation / agent-authority cures → petitioner-signed response kit |

**RFE response is a full workflow, not a footnote** (stage R, shown in the
browser stepper once active): upload the RFE letter, get the deadline
worked backward into a plan, diagnose every challenged point against its
root cause, close evidence gaps item by item, refresh citation examples
(harvested, independence-screened, highlighted PDFs), draft the letters
and the supplemental statement, and assemble the response package — with
an **emergency entry** for petitions that were NOT prepared with OpenNIW
(attorney-filed or DIY): drop in the original petition + the RFE letter
and the skill rebuilds the case file first. Every stage also bakes in
RFE-prevention rules at filing time.

## How the work is kept honest

An AI that drafts immigration arguments will produce fluent, plausible
prose whether or not the evidence is there. Most of this project is the
machinery that stops a plausible narrative from being filed as supported
evidence — distilled from the structure of real, professionally-prepared
filings and a real RFE cycle (fully de-identified, see
[docs/analysis/](docs/analysis/)) plus USCIS primary sources cited inline
with as-of dates.

### Every claim carries its evidence — and a linter checks that it does

While drafting, the agent maintains `documents/source-registry.md`: one row
per factual claim. **Load-bearing** claims — what the letter argues from,
anything about a third-party entity, anything asserting impact — carry a
full row:

| column | why it exists |
|---|---|
| **source** | exhibit number, or URL + verbatim quote + retrieval date |
| **locator** | exhibit **page and paragraph** — an officer who cannot find the proof has not been given it |
| **independent verifier** | who attests this **other than** the applicant and anyone with a stake in the outcome. `NONE — self-serving` is a legitimate answer, and a decision to make before filing, not after |
| **measure** | impact claims only: the number and its as-of date |
| **gap** | what is still missing for the claim to stand |

`openniw registry` parses that table and reports unsourced claims,
load-bearing claims with no independent verifier, missing locators, exhibit
numbers absent from the exhibit index, and cells filled with `-` / `N/A` /
`TBD` / `see above` — which look filled in and say nothing. **A
verification table that filler can satisfy is worse than no table**: it
manufactures the appearance of having checked.

The independent-verifier column exists because exhibit-binding alone misses
the real failure mode. An employer letter *is* an exhibit, so the claim
binds — and still reads as an interested party vouching for itself. That is
exactly what the RFE we studied block-quoted back as unsubstantiated.

### The citation pipeline argues depth of use, not prestige

`openniw harvest` pulls citing papers from OpenAlex; the agent then screens
for **independence** (no shared author between citing and cited paper,
surname-collisions escalated), discards anything not formally published,
**verifies in the citing full text that the citation actually exists**
(observed false-positive rate in indexes: ~5%), and scores by how the work
was used — implemented / compared-favorably / utilized / verified beats a
passing background mention. You pick the final portfolio from scored quote
cards in a browser page; `openniw highlight` produces the exhibit PDFs with
only the in-text citation and its reference-list entry marked.

Emphasizing *who* cited you actively harms a petition — it invites the
comparative test the regulations don't ask for. The pipeline is built to
argue *how*.

### The frame is frozen, and every document quotes it verbatim

The endeavor sentence (NIW), field definition and claimed criteria (EB-1A),
or petitioner structure and role (O-1) are frozen before any drafting
begins, because USCIS can treat post-filing rewording as a material change.
Lint checks that the frozen text appears identically everywhere it appears.
On an RFE for a petition prepared elsewhere, the skill extracts that text
from the as-filed record and marks it `FROZEN (as filed)` — it may never be
improved, only argued from.

### Evidence is date-classed against the priority date

Eligibility is judged as of the filing date (8 CFR 103.2(b)(12)). Every
exhibit is classed *pre-filing* / *post-filing as continuation of a named
pre-filing thread* / *not worth it*, so that at RFE time — under a
non-extendable deadline — the question of what may still be used is already
answered rather than re-litigated.

### A mock-officer pass before anything is printed

Stage V runs twelve RFE-prevention rules over the whole case from the
adjudicator's perspective (no uncorroborated third-party claims, never
expose a denominator, pre-empt "common among researchers", legal
authorities in footnotes only, and more), plus a claim-verification log
that extracts every factual claim and grades it CRITICAL (contradicts its
source) / WARNING (unsupported) / INFO, with explicit passes for the two
commonest defects: dates consistent across all documents, and titles
consistent across CV, letters, and forms.

### The agent never invents facts

Missing information becomes an explicit `[TODO]` or a question to you —
never a plausible guess. Identity numbers, dates, metrics, and quotes come
only from your sources or from you. Fields the agent derived rather than
you stating are flagged amber in the forms wizard until you confirm them.

### The engineering follows the same rule

Contract tests fail the build when documentation and code drift apart: the
61-key `answers.json` contract is enforced three ways (what the PDFs
consume ≡ what the wizard edits ≡ what the skill documents), and the RFE
stage is enforced three ways (the STATE.md line the skills tell the agent
to write ≡ the regex the browser stepper parses it with ≡ the field ids of
the data-point issue form). Skill fallback scripts are byte-compared against
their package sources. Benchmark copy is held to one wording rule
everywhere: **percentile among publicly posted approved cases, never an
individual's approval probability.**

## Filing facts (2026, verify before filing)

- NIW package: I-140 + ETA-9089 Appendix A + signed Final Determination +
  petition letter + evidence. Fees: I-140 **$715** + Asylum Program Fee
  **$300** (self-petitioner) = **$1,015**; optional premium processing
  (I-907) **$2,965**, 45 business days.
- EB-1A package: same I-140 fees ($715 + $300 self-petitioner), but **no
  ETA-9089 pages** and no ability-to-pay evidence; premium is **15
  business days** (vs NIW's 45) — and the premium lockbox state split
  *differs* from the standard split.
- O-1A package: Form I-129 + O supplement, filed by the **employer or
  agent** (never self-petitioned). I-129 (O) **$1,055** ($530 small
  employer/nonprofit) + Asylum Program Fee by employer size; premium
  **$2,965**, 15 business days; consultation letter required.
- The package README and the wizard pick the correct USCIS lockbox
  automatically (standard: Dallas/Chicago; premium: Phoenix/Elgin — premium
  filings use a *different* lockbox) and follow the USCIS-recommended
  assembly order (payment form on top, then G-1145, then the forms).
- Primary sources baked into the templates: USCIS [EB-2 page & NIW filing
  tips](https://www.uscis.gov/working-in-the-united-states/permanent-workers/employment-based-immigration-second-preference-eb-2),
  [I-140 initial-evidence checklist](https://www.uscis.gov/forms/filing-guidance/checklist-of-required-initial-evidence-for-form-i-140-for-informational-purposes-only),
  [tips for filing by mail](https://www.uscis.gov/forms/filing-guidance/tips-for-filing-forms-by-mail),
  and [I-140 direct filing addresses](https://www.uscis.gov/forms/all-forms/direct-filing-addresses-for-form-i-140-immigrant-petition-for-alien-worker).

## Privacy

- Everything runs on your machine. The case folder is the entire system of
  record — zip it, move it, or open it in any editor.
- The companion binds 127.0.0.1 only, requires a per-session random token,
  and does no AI: the only network calls in the whole system are your
  agent's own, plus the public OpenAlex API (citation metadata) and
  uscis.gov/dol.gov (blank form downloads).
- The repo contains no personal data; analyses in `docs/analysis/` are
  structural, with all identifiers replaced by placeholders.

## For maintainers

```
openniw/
├── .agents/skills/niw-petition/  # the flagship skill (EB-2 NIW)
│              └── eb1a-petition/ # EB-1A skill (beta)
│              └── o1-petition/   # O-1A skill (beta)
├── src/openniw/                  # the pip companion: FastAPI folder-mode
│   │                             #   server + CLI + committed UI bundle
│   └── ui/                       # built Next.js static export (make ui)
│   └── services/                 # deterministic compute: formfill, citations,
│                                 #   papers, package, registry linter …
├── frontend/                     # UI source (Node needed by maintainers only)
├── forms/                        # vendored official PDFs + field inventories
├── tests/                        # pytest: contracts, formfill, API, sentinel,
│                                 #   registry linter, version precision
├── scripts/                      # export_benchmark.py · sync_skill.py
└── docs/                         # design docs + de-identified analyses
```

- `make test` — full suite (63 tests). `make ui` — rebuild the UI bundle
  from `frontend/` and vendor it into the package. `make check` — tests +
  skill script sync + UI-bundle freshness. `make release` — checked wheel
  build.
- **Contract tests are the backbone.** The 61-key `answers.json` contract
  (`tests/test_contract.py`): `formfill.py` (what the PDFs consume) ≡ the
  wizard spec (what the UI edits) ≡ `references/forms.md` (what the agent
  writes). The RFE stage (`tests/test_rfe_contract.py`): the STATE.md line
  the skills document ≡ the regex `session.tsx` parses it with (lifted out
  of the TSX at test time, so changing it there fails here) ≡ the field ids
  in `.github/ISSUE_TEMPLATE/data-point.yml`.
- `openniw registry` is pure-stdlib and side-effect-free
  (`services/registry.py`) — it reads the case folder and reports; it never
  edits a user's file. Same rule for every service: the agent decides, the
  companion computes.
- Skill fallback scripts mirror package services between
  `# --- BEGIN/END SYNC ---` markers across the three petition skills;
  `scripts/sync_skill.py` regenerates them and `make check` fails on drift.
- Versions in the storage layer are **opaque strings**, never JSON numbers:
  `st_mtime_ns` exceeds `Number.MAX_SAFE_INTEGER`, so a browser silently
  rounds it and every optimistic-concurrency save 409s
  (`tests/test_version_precision.py` pins this).

## Contributing

OpenNIW is a fully open-source, free, public-interest project (开源利益众生).
It gets better through three kinds of contribution:

1. **Code** — issues and PRs welcome. High-value directions: more form
   mappings (I-907, an I-485 wizard), more browser pages (evidence ledger,
   document review), consular-processing variants, UI translations.
2. **Data points** — file the
   [anonymous data-point form](https://github.com/HHHHHejia/openniw/issues/new?template=data-point.yml)
   with your (anonymized) numbers and outcome: category, field,
   citations/papers at filing, premium choice, timeline, RFE or not,
   result — plus anything we should improve. The skills offer this as an
   optional final step, and every real data point sharpens the benchmark
   that helps the next applicant calibrate honestly.
3. **Attorneys & practitioners** — if you prepare NIW cases
   professionally, your frontier knowledge (what draws RFEs this quarter,
   what wording holds up, what evidence moves adjudicators) can be folded
   into the skill's playbooks. Open an issue or reach out directly —
   credited or anonymous, your choice.

## Contact & collaboration

- WeChat: `LittleGeng`
- X: [x.com/hejia0530](https://x.com/hejia0530)
- GitHub issues: the preferred channel for anything public

**EB-1A and O-1A are now here (beta)** — built from USCIS primary sources,
MIT-licensed open materials, and our approved-case dataset, not from
firsthand filings. That is exactly why they need you: if you have actually
been through an EB-1A or O-1 case — as applicant, or as practitioner —
your review of the playbooks is the single highest-value contribution
right now. **OpenH1B · Open-anything-immigration** — still on the wish
list; the whole framework is reusable (agent skill + local companion +
approved-case benchmark). Reach out and let's build the next one together.

## References & acknowledgments

The skills' legal and procedural content is distilled from these sources
(each skill's reference files carry inline citations with as-of dates):

**Primary sources**
- [USCIS Policy Manual](https://www.uscis.gov/policy-manual) — Vol. 6
  Part F Ch. 2 (EB-1A) & Ch. 5 (NIW), Vol. 2 Part M (O-1)
- [8 CFR 204.5](https://www.ecfr.gov/current/title-8/section-204.5) and
  [8 CFR 214.2(o)](https://www.ecfr.gov/current/title-8/section-214.2)
  via eCFR; INA via uscode.house.gov
- uscis.gov form pages, filing checklists, direct-filing-address pages, and
  the [G-1055 fee schedule](https://www.uscis.gov/g-1055);
  federalregister.gov (fee rules); travel.state.gov Visa Bulletin
- Case law: *Matter of Dhanasar*, 26 I&N Dec. 884 (AAO 2016); *Kazarian v.
  USCIS*, 596 F.3d 1115 (9th Cir. 2010); *Matter of Price*, 20 I&N Dec. 953

**Open-source projects**
- [juntoku9/claude_immigration_attorney](https://github.com/juntoku9/claude_immigration_attorney)
  (MIT) — evidence-hierarchy, expert-letter assignment matrix, RFE
  root-cause taxonomy, and national-importance research-method patterns
  were adapted with gratitude
- [razvanmarinescu/EB1A](https://github.com/razvanmarinescu/EB1A) and
  [Ryan-Rhys/EB1A](https://github.com/Ryan-Rhys/EB1A) — public approved
  self-petitions studied for structure (no text reused)

**Data & practitioner knowledge**
- [public-approval-source](https://www.public-approval-source) public approval notices
  (2012–2026) — the de-identified benchmark dataset
- Structure of real, professionally prepared NIW filings and a real RFE
  cycle (fully de-identified, see [docs/analysis/](docs/analysis/)), plus
  published analyses by immigration practitioners and university
  international offices consulted during research

## License

MIT.

## Disclaimer

OpenNIW is free software that helps you organize and prepare your own
immigration paperwork. It is a **completely open-source, free,
public-interest project** — no paid tier, no service, no upsell, ever.
To be explicit:

- **Your data never reaches us.** Your entire case is processed by YOUR
  own local AI agent in a folder on YOUR computer. Nothing is sent to us —
  we run no server that could even receive it. (The public website's
  evaluation page is fully static too: what you type stays in your
  browser.)

- **We are not attorneys and OpenNIW is not a law firm.** Nothing here is
  legal advice, and using OpenNIW creates no attorney–client relationship.
- **We charge nothing and provide no service.** There is no engagement, no
  representation, and no promise of any outcome. Immigration results
  depend on your individual facts and on adjudicator discretion.
- **You are the petitioner and remain fully responsible** for everything
  you sign and file. Review every document and form yourself before
  filing, and consider having a licensed immigration attorney review your
  case.
- **The software is provided "AS IS"**, without warranty of any kind; the
  authors and contributors accept no liability arising from its use (see
  the MIT license).
- Benchmark data reflects publicly posted, self-reported approval notices
  (successful cases only) and describes distributions of approved
  profiles — it does not predict any individual outcome.
