# OpenNIW — Design Document

Date: 2026-07-31
Status: approved-by-owner (owner pre-authorized implementation; decisions recorded here are open to revision)

## 1. Mission

OpenNIW is an open-source, AI-assisted platform that helps academics and researchers self-petition for the EB-2 National Interest Waiver (NIW) — replicating the workflow of a full-service immigration law firm, then automating away as much of the client burden as possible.

Core principle: **the user should provide links, not paperwork**. Given a Google Scholar profile, a LinkedIn export, a homepage URL, and/or a CV, the system should collect, analyze, and organize nearly everything itself, asking the user only for what cannot be derived.

> Legal disclaimer (shipped in product + README): OpenNIW is a document-preparation and self-help tool, not a law firm, and does not provide legal advice.

## 2. What a NIW filing requires (researched 2026-07)

Filing package for the I-140 stage (self-petitioner):

| Item | Notes |
|---|---|
| Form I-140 | Edition current; fee **$715** |
| Asylum Program Fee | **$300** for self-petitioners |
| ETA-9089 Appendix A | Foreign worker info; uncertified, attached to I-140 |
| ETA-9089 Final Determination page | Signed by petitioner |
| Petition Letter (PL) | Legal brief arguing the *Matter of Dhanasar* three prongs |
| Proposed Endeavor Statement (PES) | Petitioner's statement of the endeavor |
| Recommendation letters | Typically 3–6, mix of independent + dependent recommenders |
| Exhibit package | CV, degrees + evaluations, publications, citation report, evidence of Prong-2 positioning (funding, talks, reviews, adoption), etc. |
| Optional: I-907 premium processing | **$2,965** (45 business days for NIW) |
| Optional: G-1145 e-notification, G-1450 card payment, G-28 (if represented) | |

Legal framework: EB-2 baseline (advanced degree or exceptional ability) + Dhanasar prongs: (1) substantial merit & national importance; (2) well positioned to advance the endeavor; (3) on balance, beneficial to waive the job-offer/labor-cert requirement. The **Jan 15 2025 USCIS Policy Manual update** raised scrutiny: degree/field alignment with the endeavor must be shown explicitly; entrepreneur claims need concrete support (funding, contracts, letters of interest); broad "benefits the economy" assertions are insufficient. Evaluation and drafting prompts must encode this.

Post-approval flow (v1 scope: guidance only): I-485/I-765/I-131 adjustment package (forms already vendored).
RFE flow (v1 scope: analyze + draft skeleton): informed by a real RFE case in the owner's source materials.

## 3. Product flow (five stages + RFE module)

Modeled on the law firm process (free eval → retainer → questionnaire/collection → drafting → review → filing), with the questionnaire replaced by automated ingestion + a gap-filling AI interview.

**Stage 0 — Free Evaluation (no account needed to start)**
Input: email, field, degree, and any of {Google Scholar URL, homepage URL, LinkedIn profile PDF/text, CV PDF}. Backend scrapes/parses what it can (Scholar page and homepage are fetched server-side; LinkedIn is auth-walled so we accept its "Save to PDF" export or pasted text). LLM produces a structured evaluation: per-prong strengths/weaknesses, tier (strong / promising / borderline / not-yet), suggested endeavor angles, evidence gaps. This mirrors the firm's free-eval letter but is delivered instantly.

**Stage 1 — Case & evidence collection**
Eval converts into a case. The system generates a personalized evidence checklist (categories below), pre-filling items it already derived (publication list, citation metrics). Each item: upload / URL / mark-N/A. A chat-style "AI interview" asks only for missing facts (endeavor specifics, immigration history, recommender candidates).

**Stage 2 — Drafting**
Order mirrors the firm: (a) Proposed Endeavor Statement, (b) recommendation letter drafts — one per recommender, each with a distinct angle, (c) Petition Letter citing exhibits, (d) exhibit list, (e) filing cover letter. Every document: AI draft → user edits (markdown editor) → section-level regeneration → DOCX export.

**Stage 3 — Forms**
Wizard collects only still-missing biographic data, then programmatically fills I-140, ETA-9089 Appendix A + Final Determination, G-1145, and optionally I-907/G-1450 via AcroForm field mapping (all vendored PDFs verified fillable; field inventories exported to `forms/fieldmaps/*.json`).

**Stage 4 — Package assembly**
Final checklist in lockbox order (fees → forms → PL → exhibits), fee table, filing address, and a ZIP of everything.

**RFE module** — upload RFE letter → AI classifies which prongs/deficiencies are challenged → response plan + response-brief skeleton.

## 4. Architecture

Monorepo `openniw/`:

```
openniw/
├── frontend/        # Next.js (TypeScript, App Router, Tailwind) — Railway service 1
├── backend/         # FastAPI (Python 3.12) — Railway service 2
│   ├── app/
│   │   ├── routers/       # auth, eval, cases, evidence, documents, forms, chat, jobs
│   │   ├── services/      # scraping, llm, evaluation, drafting, formfill, docx_export, checklist
│   │   ├── prompts/       # versioned prompt/template files (firm-style, de-identified)
│   │   └── migrations/    # plain SQL + runner (schema_migrations table)
├── forms/           # vendored official PDFs (uscis/, dol/) + fieldmaps/*.json
└── docs/            # this spec, architecture notes, template provenance
```

Decisions:
- **DB**: Supabase Postgres via `DATABASE_URL` only (no Supabase client SDK — the provided project exposes only the pooler URL). Backend is the sole DB client through `asyncpg`; RLS unnecessary.
- **Auth**: backend-managed — email+password, passlib `pbkdf2_sha256`, JWT signed with `SECRET_KEY`, TTL from `TOKEN_TTL_HOURS` (matches env vars already provisioned).
- **AI**: OpenAI Responses API. Model `OPENAI_MODEL` (default `gpt-5.6-luna`), reasoning effort `OPENAI_REASONING_EFFORT` (default `xhigh`) per owner directive. Single `services/llm.py` chokepoint with JSON-schema-constrained outputs for structured tasks.
- **Long jobs** (eval, drafting): `jobs` table + FastAPI background tasks; frontend polls. No Celery/queue in v1.
- **File storage**: local `DATA_DIR` (Railway volume). Storage adapter kept behind one module so Supabase Storage can be swapped in later.
- **Deploy**: two Railway services from Dockerfiles; `railway.json` per service; env via Railway variables. Never commit `.env`.

## 5. Data model (Postgres)

users(id, email uniq, password_hash, created_at)
cases(id, user_id, title, field, stage: eval|collect|draft|forms|package|rfe, created_at)
profiles(case_id PK, scholar_url, homepage_url, raw jsonb, parsed jsonb, metrics jsonb, updated_at)
evaluations(id, case_id, input_snapshot jsonb, report_md, tier, prong_scores jsonb, created_at)
evidence_items(id, case_id, category, title, description, status: suggested|needed|provided|na, source_url, file_path, ai_notes, exhibit_no)
recommenders(id, case_id, name, title, org, relationship: independent|dependent, angle, email, status)
documents(id, case_id, doc_type: pes|petition_letter|reco_letter|exhibit_list|cover_letter|rfe_response, recommender_id?, version, content_md, status: draft|reviewed|final, created_at)
form_data(case_id PK, answers jsonb, updated_at)
filled_forms(id, case_id, form_code, file_path, created_at)
jobs(id, case_id?, kind, status: queued|running|done|error, payload jsonb, result jsonb, error, created_at, updated_at)
messages(id, case_id, role, content, created_at)   -- AI intake interview
uploads(id, case_id, kind: cv|linkedin|degree|rfe|other, filename, file_path, text_extract, created_at)

## 6. Evidence categories (checklist taxonomy)

identity/status · degrees & transcripts · CV · publication list · citation report (Scholar) · peer-review record · recommendation letters · awards/honors · memberships · media coverage · funding/grants · patents/IP · talks & invited lectures · adoption/implementation evidence · endeavor-support evidence (letters of interest, contracts, funding) — refined against the firm's client packet once source-material analysis completes.

## 7. Privacy & open-source hygiene

- Templates/prompts derived from the owner's law-firm materials are **structure only** — no personal data, no verbatim firm-proprietary text; provenance noted in `docs/templates.md`.
- `.gitignore` excludes `.env`, uploads, `DATA_DIR`.
- License: MIT. Disclaimer everywhere user-facing.

## 8. Testing

- Unit: form field-mapping (assert every mapped field exists in fieldmap JSON), checklist generation, auth.
- Integration: eval pipeline with a fixture profile (LLM mocked), form-fill produces a readable PDF with expected values.
- Manual E2E against live LLM before release.

## 9. Out of scope (v1)

Payments, multi-user firms/agents mode, e-filing integration (USCIS has no API; output is print-and-mail package), consular processing variants, non-academic entrepreneur deep support (guidance only), Supabase Auth/Storage/RLS.
