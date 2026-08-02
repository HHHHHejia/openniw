# OpenNIW

**Open-source, AI-assisted EB-2 National Interest Waiver (NIW) self-petitions —
from a free evaluation of your public record to a complete filing package.**

OpenNIW replicates the workflow of a full-service NIW law firm, then automates
away the paperwork. The core principle: **you give links, not paperwork.**
From a Google Scholar profile, a homepage URL, and/or a CV, the system
collects, analyzes, and organizes nearly everything itself, asking you only
for what it cannot derive.

> **OpenNIW is a document-preparation and self-help tool, not a law firm, and
> does not provide legal advice.** Immigration outcomes depend on individual
> facts and adjudicator discretion. Review everything before filing; consider
> consulting a licensed attorney.

## The five stages

| Stage | What happens |
|---|---|
| **I — Evaluate** | Paste your Scholar link / homepage / CV → instant structured evaluation: tier, prong-by-prong strengths and gaps, suggested endeavor angles. Free, no account needed. |
| **II — Collect** | The evaluation becomes a case. A personalized evidence checklist is generated; the system pre-fills what it derived (publications, citations, metrics). A chat-style AI interview asks only for what's missing. |
| **III — Draft** | Proposed Endeavor Statement → support letters → Petition Letter (Dhanasar three-prong brief, cited to exhibits) → Index of Exhibits → cover letter. Markdown editing, versioning, DOCX export. |
| **IV — Forms** | One wizard fills the official PDFs programmatically: I-140, ETA-9089 Appendix A + Final Determination, G-1145. AI pre-fills the wizard from your record. |
| **V — File** | A ZIP in lockbox order with the fee table, filing address guidance, and an assembly checklist. Print, sign, mail. |

Plus an **RFE module**: paste an RFE letter and get a structured response plan
(which prongs are challenged, officer errors to rebut, an evidence plan, and a
supplemental-statement outline).

### v0.2 automation

- **Citation pipeline** — the most labor-intensive part of a NIW case,
  automated: every citing paper is harvested from OpenAlex, screened for
  independence (same-surname collisions escalated for review), verified to
  actually cite the work in its full text, LLM-scored by depth of use
  (implemented / compared-favorably / utilized / verified, HOW > WHO),
  negative citations quarantined, a portfolio selected across cited works,
  and delivered as highlighted PDFs + a Citation Examples control document +
  independent-recommender candidates drawn from citing authors.
- **Evidence auto-intake** — any uploaded file is classified (diploma,
  review email, award page…), matched to the checklist, key facts extracted
  into a canonical fact table, and date-classed against the filing date.
- **Endeavor composer** — the one frozen sentence, built from three bounded
  inputs (method / topic / impact), AI-polished into candidates and scored
  against the six executability elements; freezing locks the wording for
  every drafted document.
- **Streaming evaluation** — the free evaluation streams live (SSE) with
  stage progress and prong-score bars.
- **Forms wizard** — structured repeating-group editors and per-field "AI"
  marks after pre-fill, cleared as you review.

## What makes the drafting good

The templates and heuristics are distilled from the structure of real,
professionally-prepared NIW filings and a real RFE cycle (fully de-identified —
see [docs/analysis/](docs/analysis/)):

- The petition letter follows the exact section architecture and module stacks
  strong filings use (advanced degree → Prong 1 policy-anchored modules →
  Prong 2 quantitative modules → Prong 3 balancing factors → 3-group exhibit
  index).
- The **endeavor sentence is treated as frozen**: composed once
  (method + topic + impact), then repeated verbatim — USCIS treats rewording
  as a potential material change.
- RFE-prevention rules are built in: no uncorroborated third-party claims,
  no denominators that diminish you, foreign affiliations trigger
  documentation requirements, Prong 3 is built from facts, and legal
  authorities go in footnotes.
- The AI never invents facts — anything missing becomes an explicit `[TODO]`.

## Architecture

```
openniw/
├── frontend/   Next.js 14 + Tailwind (Node.js)      — Railway service 1
├── backend/    FastAPI (Python 3.12) + asyncpg      — Railway service 2
│   └── app/
│       ├── routers/     auth, eval, cases, evidence, documents,
│       │                recommenders, chat, ingest, forms, jobs
│       ├── services/    llm, scraping, evaluation, checklist, drafting,
│       │                formfill, docx_export, storage, jobs, forms_spec
│       ├── prompts/     versioned drafting/eval prompt templates
│       └── migrations/  plain SQL, applied automatically at startup
├── forms/      vendored official USCIS/DOL PDFs + field inventories (JSON)
├── .agents/skills/niw-petition/   the Agent Skill (run mode 3); .claude/skills symlinks here
└── docs/       design doc + de-identified structural analyses
```

- **Database**: Postgres (Supabase works out of the box via `DATABASE_URL`).
  All tables live in a dedicated `openniw` schema; every query runs with
  `SET LOCAL search_path`, so pooled/pgbouncer connections are safe and a
  shared database is never polluted.
- **Auth**: email+password, pbkdf2, JWT.
- **AI**: OpenAI Responses API. Model and reasoning effort are env-configured
  (`OPENAI_MODEL`, default `gpt-5.6-luna`; `OPENAI_REASONING_EFFORT`, default
  `xhigh`). One chokepoint module (`services/llm.py`).
- **Form filling**: the vendored official PDFs are AcroForm-fillable; field
  inventories are exported to `forms/fieldmaps/*.json` and mapped from one
  flat semantic answer model (`services/formfill.py`). Unmapped fields are
  reported, never silently dropped.
- **Long jobs** (evaluation, drafting): a `jobs` table + background tasks;
  the frontend polls.

## Three ways to run OpenNIW

### 1 · Hosted (zero setup)

Use the maintained deployment — nothing to install:

- App: https://frontend-production-3c7f.up.railway.app
- API: https://backend-production-9b6c.up.railway.app (health: `/health`, docs: `/docs`)

### 2 · Self-hosted (your keys, your database, your machine)

The only outbound traffic is to your own OpenAI account and the public
OpenAlex API — never to any maintainer server:

```bash
git clone https://github.com/HHHHHejia/openniw && cd openniw
cp .env.example .env
# in .env, set:
#   OPENAI_API_KEY=sk-...
#   SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
docker compose up --build
open http://localhost:3000
```

A local Postgres is bundled — you don't need Supabase. To use your own
Postgres/Supabase instead, uncomment `DATABASE_URL` in `.env` (all tables go
into a dedicated `openniw` schema, so a shared database stays clean).

Without Docker (Python 3.12+, Node 20+):

```bash
cd backend && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp ../.env.example .env   # here DATABASE_URL is required (no bundled db), plus SECRET_KEY, OPENAI_API_KEY
.venv/bin/uvicorn app.main:app --port 8400    # migrations run automatically
# new terminal:
cd frontend && npm install && NEXT_PUBLIC_API_URL=http://localhost:8400 npm run dev
```

Deploy your own cloud copy on Railway: two services from this repo —
**backend** (config `backend/railway.json`; vars `DATABASE_URL`, `SECRET_KEY`,
`OPENAI_API_KEY`, `CORS_ORIGINS=https://<frontend-domain>`, `DATA_DIR=/data`
+ a volume at `/data`) and **frontend** (config `frontend/railway.json`;
`NEXT_PUBLIC_API_URL=https://<backend-domain>`).

### 3 · Agent Skill (no server, no database, no API key)

The whole workflow also ships as an [Agent Skill](https://agentskills.io) at
[.agents/skills/niw-petition/](.agents/skills/niw-petition/): your coding
agent (Claude Code, Codex, Cursor, …) becomes the NIW paralegal, a local
folder is the case file, and your existing AI subscription does the drafting
— bundled scripts handle the deterministic parts (official-form download and
filling, OpenAlex citation harvesting).

```bash
# easiest — cross-agent installer (Claude Code, Codex, Cursor, 70+ agents):
npx skills add HHHHHejia/openniw

# or manually — Claude Code:
git clone https://github.com/HHHHHejia/openniw
mkdir -p ~/.claude/skills && cp -r openniw/.agents/skills/niw-petition ~/.claude/skills/

# or manually — Codex (and other Agent-Skills tools; Cursor also reads ~/.cursor/skills):
mkdir -p ~/.agents/skills && cp -r openniw/.agents/skills/niw-petition ~/.agents/skills/
```

(On Windows, prefer `npx skills add` or the manual copy — the repo's
`.claude/skills` symlink needs symlink support to work from a checkout.)

Then just say "帮我准备 NIW 申请" / "evaluate my NIW case" in your agent. It
follows the same five stages — evaluate → endeavor → evidence (the agent
itself scores citations; no OpenAI key needed) → draft → forms & package —
writing everything into a `niw-case/` folder you own. Progressive disclosure
keeps it light: per-stage reference files load only when that stage begins.

## Filing facts (2026, verify before filing)

- NIW package: I-140 + ETA-9089 Appendix A + signed Final Determination +
  petition letter + evidence. Fees: I-140 **$715** + Asylum Program Fee
  **$300** (self-petitioner) = **$1,015**; optional premium processing (I-907)
  **$2,965**, 45 business days.
- Jan 15, 2025 USCIS Policy Manual update raised scrutiny: degree–endeavor
  alignment must be explicit; broad economy-benefit claims are insufficient;
  entrepreneur claims need concrete support. OpenNIW's evaluation and
  drafting encode this.

## Privacy

- Self-hosted: your data lives in **your** database and **your** OpenAI
  account. The only third-party calls are your OpenAI API and the public
  OpenAlex API (citation metadata); nothing goes to any maintainer server.
  The skill mode needs no API key at all — your coding agent does the work.
- The repo contains no personal data. Analyses in `docs/analysis/` are
  structural only, with all identifiers replaced by placeholders.
- Never commit `.env`; see `.env.example`.

## Contributing

Issues and PRs welcome. High-value directions: citation-pipeline automation
(harvest → verify → independence → depth-scoring), ESI-style percentile data
sources, more form mappings (I-907, I-485 family), consular-processing
variants, translations of the UI.

## License

MIT. 开源利益众生 — built so that strong researchers can afford a strong
petition.
