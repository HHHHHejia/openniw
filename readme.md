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

## Run it locally

Prereqs: Python 3.12+, Node 20+, a Postgres URL (free Supabase project works).

```bash
# 1. Backend
cd backend
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp ../.env.example .env        # fill in DATABASE_URL, SECRET_KEY, OPENAI_API_KEY
.venv/bin/uvicorn app.main:app --port 8400   # migrations run automatically

# 2. Frontend (new terminal)
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8400 npm run dev
```

Open http://localhost:3000.

## Live deployment

- App: https://frontend-production-3c7f.up.railway.app
- API: https://backend-production-9b6c.up.railway.app (health: `/health`, docs: `/docs`)

## Deploy on Railway

Two services from one repo:

1. **backend** — root directory `/`, config `backend/railway.json`
   (Dockerfile build). Set env vars: `DATABASE_URL`, `SECRET_KEY`,
   `OPENAI_API_KEY`, `CORS_ORIGINS=https://<your-frontend-domain>`,
   `DATA_DIR=/data` + attach a volume at `/data`.
2. **frontend** — config `frontend/railway.json`. Set build arg / env
   `NEXT_PUBLIC_API_URL=https://<your-backend-domain>`.

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
  account. Nothing is sent anywhere else.
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
