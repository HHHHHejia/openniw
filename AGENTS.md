# OpenNIW — agent instructions

Open-source AI-assisted EB-2 NIW (National Interest Waiver) petition
preparation. The product is an Agent Skill plus a pip companion:
`.agents/skills/niw-petition/` (the skill — the single entry point) ·
`src/openniw/` (the `openniw` pip package: localhost browser UI +
deterministic compute over a case folder) · `frontend/` UI source (Next.js
14, maintainers only) · `forms/` vendored official USCIS/DOL fillable PDFs +
field maps · `docs/` design + de-identified structural analyses.

## The NIW petition skill

Codex, Cursor and other Agent-Skills tools discover the skill at
`.agents/skills/niw-petition/` automatically; `.claude/skills` symlinks to
the same folder for Claude Code. If the user asks to prepare, evaluate, or
fix a NIW/EB-2 petition, use that skill — it runs the whole workflow in a
local case folder with no server, no database, and no API keys.

## Working on the code

- Companion package: `pip install -e .` then `openniw --version`.
  Run tests: `make test` (pytest over `tests/`).
- The case folder is the only storage; `src/openniw/casefolder.py` is the
  storage layer (atomic writes, mtime versions, events log). The UI-session
  sentinel protocol lives in `src/openniw/ui_session.py` — the skill's
  Browser-sessions section in SKILL.md must stay in sync with it.
- UI: `make ui` rebuilds `frontend/` and vendors the static export into
  `src/openniw/ui/` (committed; Node is a maintainer-only dependency).
  Never name build dirs `out/` or `dist/` inside `src/` — .gitignore eats
  them.
- The 61-key `answers.json` contract is enforced by
  `tests/test_contract.py` across formfill.py ≡ forms_spec.WIZARD ≡ the
  skill's `references/forms.md`. Extending forms? Update all three, plus
  `forms/fieldmaps/*.json` inventories; report unmatched fields, never drop
  silently.
- Skill fallback scripts mirror package services between
  `# --- BEGIN/END SYNC ---` markers — edit the package source, then run
  `python3 scripts/sync_skill.py`; `make check` fails on drift.
- There is no LLM anywhere in this repo's runtime: the user's agent is the
  AI. Do not add API-key dependencies.
- Domain rules (frozen endeavor sentence, no uninvented facts, exhibit
  binding, citation doctrine) are documented in `docs/analysis/` — read
  before changing skill references or drafting guidance.
