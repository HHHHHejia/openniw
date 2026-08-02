# OpenNIW — agent instructions

Open-source AI-assisted EB-2 NIW (National Interest Waiver) petition
preparation. Monorepo: `backend/` FastAPI (Python 3.12) · `frontend/`
Next.js 14 · `forms/` vendored official USCIS/DOL fillable PDFs + field maps
· `docs/` design + de-identified structural analyses of real filings.

## The NIW petition skill

This repo ships an Agent Skill at `.agents/skills/niw-petition/` (Codex,
Cursor and other Agent-Skills tools discover it here automatically;
`.claude/skills` symlinks to the same folder for Claude Code). If the user
asks to prepare, evaluate, or fix a NIW/EB-2 petition, use that skill — it
runs the whole workflow in a local case folder with no server or database.

## Working on the code

- Backend: `cd backend && .venv/bin/uvicorn app.main:app --port 8400`
  (migrations run at startup; needs `.env` — see `.env.example`).
  All DB tables live in the dedicated `openniw` Postgres schema; every query
  runs with `SET LOCAL search_path` (pooled/pgbouncer-safe). No ORM — plain
  SQL via `app/db.py` helpers.
- Frontend: `cd frontend && npm run dev` (talks to
  `NEXT_PUBLIC_API_URL`, default http://localhost:8400).
- Full self-hosted stack: `docker compose up --build` (bundles Postgres).
- All LLM calls go through `backend/app/services/llm.py`; prompts live in
  `backend/app/prompts/*.md`. Never hardcode secrets; never commit `.env`.
- Form-filling maps flat semantic answer keys onto PDF field names —
  inventories in `forms/fieldmaps/*.json`; report unmatched fields, never
  drop silently.
- Domain rules (frozen endeavor sentence, no uninvented facts, exhibit
  binding, citation doctrine) are documented in `docs/analysis/` — read
  before changing prompts or drafting logic.
