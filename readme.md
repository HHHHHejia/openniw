# OpenNIW

**A free, open-source tool that helps you organize and speed up your own
EB-2 National Interest Waiver (NIW) self-petition — your coding agent does
the organizing, a local folder is the case file, and a browser wizard
appears exactly when a GUI beats chat.**

Website: **[openniw.com](https://openniw.com)** — project intro, install
guide, and a free no-signup statistical evaluation against 7,458 approved cases
(fully static; source in [webpage/](webpage/)).

OpenNIW is an [Agent Skill](https://agentskills.io). Install it into
Claude Code, Codex, Cursor, or any Agent-Skills tool, and your existing AI
subscription runs the entire preparation workflow — evaluation, evidence,
drafting, official forms, filing package — with **zero configuration**:

- **No account.** Nothing to sign up for.
- **No database.** Your case lives in a `niw-case/` folder you own.
- **No API key.** Your agent's subscription is the AI.
- **No server.** A localhost companion opens only when you reach a
  form-heavy step, and only talks to your case folder.

> **OpenNIW is a document-preparation and self-help tool, not a law firm, and
> does not provide legal advice.** Immigration outcomes depend on individual
> facts and adjudicator discretion. Review everything before filing; consider
> consulting a licensed attorney.

## Install

```bash
# cross-agent installer (Claude Code, Codex, Cursor, 70+ agents):
npx skills add HHHHHejia/openniw

# or manually — Claude Code:
git clone https://github.com/HHHHHejia/openniw
mkdir -p ~/.claude/skills && cp -r openniw/.agents/skills/niw-petition ~/.claude/skills/

# or manually — Codex and other Agent-Skills tools:
mkdir -p ~/.agents/skills && cp -r openniw/.agents/skills/niw-petition ~/.agents/skills/
```

Then say **"帮我准备 NIW 申请"** or **"evaluate my NIW case"** in your agent.

## How it works

```
        ┌──────────────────────────────────────┐
        │   Your agent + the niw-petition      │   the BRAIN — conversation,
        │   skill (Claude Code / Codex / …)    │   judgment, drafting, prefill
        └──────┬─────────────────────┬─────────┘
   reads/writes│                     │ launches at interaction-heavy steps
               ▼                     ▼
        ┌────────────┐   ┌───────────────────────────┐
        │ niw-case/  │◄──┤ openniw (pip companion)   │  the ORGAN — browser
        │ STATE.md   │   │ localhost form wizard +   │  wizard & deterministic
        │ case.json  │   │ citation review + PDF     │  compute; zero LLM,
        │ forms/ …   │   │ fill / package / harvest  │  zero keys, zero DB
        └────────────┘   └───────────────────────────┘
```

- The **skill** drives all five stages and survives weeks of short sessions:
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
  never a requirement.

## The five stages

| Stage | What happens |
|---|---|
| **I — Evaluate** | Paste your Scholar link / homepage / CV → tiered, prong-by-prong evaluation with strengthening plan. |
| **II·a — Endeavor** | Compose and FREEZE the one canonical endeavor sentence (method + topic + impact) — every document quotes it verbatim. |
| **II·b — Evidence** | Personalized checklist; citation pipeline (harvest → independence screen → the agent verifies full text and scores depth of use → browser review to pick the portfolio). |
| **III — Draft** | Proposed Endeavor Statement → support letters → Petition Letter (Dhanasar three-prong brief, cited to exhibits) → Index of Exhibits. |
| **IV — Forms** | The agent pre-fills `forms/answers.json` (never guessing identity numbers), then opens the browser wizard: review amber AI fields, fill the official PDFs, inspect them live. |
| **V — Package** | Twelve-rule RFE red-team pass, then the ZIP in lockbox order with fees and the correct USCIS lockbox address picked by state + premium status. |

Plus an **RFE module**: paste an RFE letter and get a structured response
plan and supplemental-statement outline.

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
- The AI never invents facts — anything missing becomes an explicit `[TODO]`
  or a question to you.

## Filing facts (2026, verify before filing)

- NIW package: I-140 + ETA-9089 Appendix A + signed Final Determination +
  petition letter + evidence. Fees: I-140 **$715** + Asylum Program Fee
  **$300** (self-petitioner) = **$1,015**; optional premium processing
  (I-907) **$2,965**, 45 business days.
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
├── .agents/skills/niw-petition/  # the skill (the product's entry point)
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

**OpenO1 · OpenEB1A · OpenH1B · Open-anything-immigration** — we would
love to build them, but they are beyond our firsthand knowledge. The
whole framework is reusable (agent skill + local companion + approved-case
benchmark); what each new category needs is someone who has actually been
through it — an applicant with a filed case, or a practitioner. If that's
you, reach out and let's build the next one together.

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
