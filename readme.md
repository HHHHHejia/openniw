# OpenNIW — NIW · EB-1A · O-1

**Free, open-source agent skills that help you organize and speed up your
own U.S. immigration petition — the EB-2 NIW and EB-1A self-petitions, and
the O-1A petition kit. Your coding agent does the organizing, a local
folder is the case file, and a browser wizard appears exactly when a GUI
beats chat.**

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

OpenNIW ships three [Agent Skills](https://agentskills.io) —
`niw-petition`, `eb1a-petition`, and `o1-petition`. Install them into
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
# offers all three skills; install what you need:
npx skills add HHHHHejia/openniw

# or manually — Claude Code (swap in eb1a-petition / o1-petition as needed):
git clone https://github.com/HHHHHejia/openniw
mkdir -p ~/.claude/skills && cp -r openniw/.agents/skills/niw-petition ~/.claude/skills/

# or manually — Codex and other Agent-Skills tools:
mkdir -p ~/.agents/skills && cp -r openniw/.agents/skills/niw-petition ~/.agents/skills/
```

Then say **"帮我准备 NIW 申请"** or **"evaluate my NIW case"** in your
agent — or "evaluate my EB-1A case" / "prepare my O-1 petition" for the
sibling skills.

## The three skills

| Skill | Category | Status | What differs |
|---|---|---|---|
| `niw-petition` | EB-2 NIW self-petition (I-140 + ETA-9089 App. A) | shipped | Full flow incl. browser forms wizard, deterministic PDF fill, filing-package ZIP |
| `eb1a-petition` | EB-1A extraordinary ability self-petition (I-140, E11) | beta | All ten 8 CFR 204.5(h)(3) criteria, Kazarian two-step petition letter with Final Merits section, benchmark vs ~2,300 approved EB-1A cases; I-140 by field guide (wizard = roadmap) |
| `o1-petition` | O-1A petition kit (I-129; employer / agent / founder-owned entity) | beta | Petitioner-structure decision tree, consultation/advisory opinion, itinerary, signature-ready hand-off package for the petitioner; I-129 by field guide |

The beta skills were built from primary sources (USCIS Policy Manual, 8 CFR,
current fee schedules — all cited inline with as-of dates), open-source MIT
materials, and our 7,458-case approved-case dataset. They follow the same
frozen-frame doctrine, exhibit-bound drafting, and RFE red-team pass as the
NIW flagship. **If you have been through an EB-1A or O-1 filing —
applicant or practitioner — we would love your review.**

## How it works

```
        ┌──────────────────────────────────────┐
        │   Your agent + a petition skill      │   the BRAIN — conversation,
        │   (niw / eb1a / o1 · any agent)      │   judgment, drafting, prefill
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

- Each **skill** drives all six stages and survives weeks of short sessions:
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

## The six stages

All three skills follow the same shape; each stage adapts to its law:

| Stage | NIW | EB-1A | O-1A |
|---|---|---|---|
| **I — Evaluate** | Tiered, Dhanasar prong-by-prong read | All ten 204.5(h)(3) criteria + Kazarian two-step test | 8 O-1A criteria + petitioner-feasibility read |
| **II·a — Frame** | FREEZE the canonical endeavor sentence | FREEZE field definition + target criteria + continue-work statement | FREEZE petitioner structure + field + role/itinerary + consultation plan |
| **II·b — Evidence** | Personalized checklist; citation pipeline (harvest → independence screen → full-text verify → browser portfolio pick) — shared by all three | ← same | ← same, plus contracts / deal memos / itinerary |
| **III — Draft** | PES → support letters → Dhanasar three-prong Petition Letter → exhibit index | Continue-work statement → letters → Kazarian two-step letter with Final Merits section | Petitioner support letter → consultation request → itinerary → expert letters |
| **IV — Forms** | Browser wizard over the 61-field answer set → deterministic I-140/ETA-9089 PDF fill | I-140 (E11) field-by-field guide | I-129 + O supplement field guide |
| **V — Package** | ZIP in lockbox order, state+premium-aware address | Assembly checklist, standard-vs-premium lockbox tables | Signature-ready hand-off kit for the petitioner |

Every skill starts each stage with an RFE-prevention mindset and includes a
full **RFE module**: paste an RFE letter and get a structured response plan
and supplemental-statement outline.

## What makes the drafting good

The templates and heuristics are distilled from the structure of real,
professionally-prepared NIW filings and a real RFE cycle (fully de-identified —
see [docs/analysis/](docs/analysis/)):

- The petition letter follows the exact section architecture strong filings
  use (advanced degree → Prong 1 policy-anchored modules → Prong 2
  quantitative modules → Prong 3 balancing factors → 3-group exhibit index).
- The **endeavor sentence is treated as frozen** — USCIS treats rewording as
  a potential material change.
- RFE-prevention rules are built in: no uncorroborated third-party claims,
  no diminishing denominators, citation depth over citer prestige, legal
  authorities in footnotes, and a pre-filing mock-officer pass.
- The EB-1A and O-1A letters follow their categories' expected
  architectures — the Kazarian two-step brief with an explicit Final
  Merits section, and the criterion-by-criterion petitioner support
  letter with consultation package — built from cited primary sources
  and MIT-licensed open materials (see References & acknowledgments).
- The AI never invents facts — anything missing becomes an explicit `[TODO]`
  or a question to you.

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
├── frontend/                     # UI source (Node needed by maintainers only)
├── forms/                        # vendored official PDFs + field inventories
├── tests/                        # pytest: contract, formfill, API, sentinel
└── docs/                         # design docs + de-identified analyses
```

- `make test` — full suite. `make ui` — rebuild the UI bundle from
  `frontend/` and vendor it into the package. `make check` — tests + skill
  script sync + UI-bundle freshness. `make release` — checked wheel build.
- The 61-key `answers.json` contract is enforced three ways by
  `tests/test_contract.py`: `formfill.py` (what PDFs consume) ≡ the wizard
  spec (what the UI edits) ≡ `references/forms.md` (what the agent writes).
- Skill fallback scripts mirror package services between
  `# --- BEGIN/END SYNC ---` markers; `scripts/sync_skill.py` regenerates
  them and `make check` fails on drift.

## Contributing

OpenNIW is a fully open-source, free, public-interest project (开源利益众生).
It gets better through three kinds of contribution:

1. **Code** — issues and PRs welcome. High-value directions: more form
   mappings (I-907, I-485 family), more browser pages (evidence ledger,
   document review), consular-processing variants, UI translations.
2. **Data points** — open an issue with your (anonymized) numbers and
   outcome: category, field, citations/papers at filing, premium choice,
   timeline, RFE or not, result. Every real data point sharpens the
   benchmark that helps the next applicant calibrate honestly.
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
