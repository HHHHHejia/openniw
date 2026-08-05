# OpenNIW — agent instructions

Open-source AI-assisted U.S. immigration petition preparation. The product
is four sibling Agent Skills plus a pip companion:
`.agents/skills/niw-petition/` (EB-2 NIW — the flagship) ·
`.agents/skills/eb1a-petition/` (EB-1A, beta) ·
`.agents/skills/o1-petition/` (O-1A, beta) ·
`.agents/skills/i485-adjustment/` (employment-based I-485, beta) ·
`src/openniw/` (the `openniw` pip package: localhost browser UI +
deterministic compute over a case folder) · `frontend/` UI source (Next.js
14, maintainers only) · `forms/` vendored official USCIS/DOL fillable PDFs +
field maps · `docs/` design + de-identified structural analyses.

## The petition skills

Codex, Cursor and other Agent-Skills tools discover the skills under
`.agents/skills/` automatically; `.claude/skills` symlinks to the same
folder for Claude Code. NIW/EB-2 requests → `niw-petition`; EB-1A /
extraordinary-ability green card → `eb1a-petition`; O-1/O-1A visa →
`o1-petition`; adjustment of status on an employment-based I-140 →
`i485-adjustment`. Each runs its whole workflow in a local case folder with
no server, no database, and no API keys. The browser wizard + PDF fill
(`openniw fill` / `ui forms` / `package`) are NIW-only; the sibling skills
use guided chat + field guides for their forms stages.

`i485-adjustment` is deliberately shaped differently from the petition
skills: it is an **assembly and completeness tool, not an eligibility
tool**. A 2026 I-485 denial for someone without other status can lead to a
Notice to Appear, so the skill hard-stops on inadmissibility (Form I-485
Part 9), criminal history, overstay/unauthorized work, 245(k)/245(c)
day-counts, CSPA, 204(j), and the decision to *use* an EAD or advance
parole. Those refusals are the product — `tests/test_i485_contract.py`
pins them, along with the Part 9 numbering and a copyright scan over the
source material the research drew on. Family-based I-485 is out of scope.

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
