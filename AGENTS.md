# OpenNIW — agent instructions

Open-source AI-assisted U.S. immigration petition preparation. The product
is three sibling Agent Skills plus a pip companion:
`.agents/skills/niw-petition/` (EB-2 NIW — the flagship) ·
`.agents/skills/eb1a-petition/` (EB-1A, beta) ·
`.agents/skills/o1-petition/` (O-1A, beta) ·
`src/openniw/` (the `openniw` pip package: localhost browser UI +
deterministic compute over a case folder) · `frontend/` UI source (Next.js
14, maintainers only) · `forms/` vendored official USCIS/DOL fillable PDFs +
field maps · `docs/` design + de-identified structural analyses.

## The petition skills

Codex, Cursor and other Agent-Skills tools discover the skills under
`.agents/skills/` automatically; `.claude/skills` symlinks to the same
folder for Claude Code. NIW/EB-2 requests → `niw-petition`; EB-1A /
extraordinary-ability green card → `eb1a-petition`; O-1/O-1A visa →
`o1-petition`. Each runs its whole workflow in a local case folder with no
server, no database, and no API keys. The browser wizard + PDF fill
(`openniw fill` / `ui forms` / `package`) are NIW-only; the sibling skills
use guided chat + field guides for their forms stages.

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
  `# --- BEGIN/END SYNC ---` markers — across ALL THREE skills — edit the
  package source, then run `python3 scripts/sync_skill.py`; `make check`
  fails on drift. Category-specific scripts (eb1a `fetch_forms.py`,
  o1 `fetch_forms_o1.py`) are standalone adaptations, deliberately
  unmanaged.
- There is no LLM anywhere in this repo's runtime: the user's agent is the
  AI. Do not add API-key dependencies.
- Domain rules (frozen endeavor sentence, no uninvented facts, exhibit
  binding, citation doctrine) are documented in `docs/analysis/` — read
  before changing skill references or drafting guidance.
