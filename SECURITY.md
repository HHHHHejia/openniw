# Security & data handling

OpenNIW is software you run on your own machine to prepare your own
immigration paperwork. It handles some of the most sensitive data a person
has — passport numbers, A-Numbers, dates of birth, immigration history — so
this page states exactly what it does with them, and what it never does.

## Your data

**Nothing leaves your computer.** There is no OpenNIW account, no OpenNIW
server, no telemetry, no analytics, and no crash reporting. The maintainers
cannot see your case, because there is nowhere for it to go. Your case is a
folder you own; zip it, move it, or delete it, and nothing is left behind
anywhere else.

The AI that reads your case is **your own agent subscription** (Claude Code,
Codex, Cursor, …). Your prompts go to that provider under your own account
and their terms, exactly as they would if you used the agent for anything
else. OpenNIW adds no key, no proxy, and no intermediary.

## Every network call the system can make

There are exactly four, all of them to named public endpoints, all
initiated by you or your agent:

| Destination | Why | Which component |
|---|---|---|
| `api.openalex.org` | citation and paper metadata for the citation pipeline | `openniw harvest`, `openniw papers` |
| open-access paper hosts (arXiv, PMC, publisher OA links found via OpenAlex) | downloading your own papers into `sources/papers/` | `openniw papers` |
| `uscis.gov`, `dol.gov` | downloading the official blank form PDFs | `openniw fetch-forms` |
| your agent's own provider | the AI itself | your agent, not OpenNIW |

The benchmark dataset ships inside the package; comparing yourself against
it is pure local computation. The desktop app's embedded views are
hard-limited to `127.0.0.1` in code.

## The localhost companion

Some steps open a browser page served by the `openniw` companion. That
server:

- binds `127.0.0.1` only — never `0.0.0.0`, so nothing on your network can
  reach it;
- requires a random per-session token in the URL, and checks the `Host` and
  `Origin` headers;
- sends `Cache-Control: no-store`;
- reads and writes **only inside your case folder** — uploads are
  traversal-checked, never clobber existing files, and are size-capped;
- contains no LLM, no key, no account, and no database.

## Commands the skills may run

Agent skills are instructions, so it matters what they instruct. These are
all of the external commands the four skills can ask your agent to run:

- `uv tool install openniw` / `pipx install openniw` /
  `python3 -m pip install --user openniw` — installing this project's own
  companion, published from this repository;
- `pip install pypdf cryptography` — only for the offline PDF-filling
  fallback;
- `git clone https://github.com/HHHHHejia/openniw ~/openniw` then
  `npm install` — **only if you ask for the optional desktop window**, and
  only from this project's own repository.

Nothing else is installed, downloaded, or executed. No skill reads
`~/.ssh`, `.env` files, keychains, browser profiles, or any credential
store, and none is capable of sending your case anywhere.

## What the skills deliberately refuse to do

- `i485-adjustment` stops rather than guess on inadmissibility (Form I-485
  Part 9), criminal history, overstay or unauthorized work, 245(k)/245(c)
  day-counts, CSPA, and the decision to use an EAD or advance parole.
- No skill will help you phrase around, minimise, or omit a fact that cuts
  against you.
- No skill invents facts: missing information becomes an explicit `[TODO]`
  or a question to you.

These refusals are enforced by tests (`tests/test_i485_contract.py`,
`tests/test_ui_host.py`, `tests/test_contract.py`).

## Reporting a problem

Open an issue at
<https://github.com/HHHHHejia/openniw/issues>. If you believe you have
found something with security impact and would rather not post it publicly,
say so in a minimal issue ("security report, please make contact") and you
will be contacted; do not include your case data or any personal
identifiers in the report.

## A note on automated risk scores

Third-party scanners flag these skills for handling sensitive personal
identifiers and for instructing package installation. Both are true and
intended: preparing an I-485 requires an A-Number and a passport number,
and the companion has to be installed to fill a PDF. The mitigation is not
to hide those facts but to keep them local and auditable — which is what
this page, and roughly 3,000 lines of readable markdown and Python in this
repository, are for. If a scanner reports something concrete that this page
does not explain, please open an issue; that would be a real finding and it
will be fixed.
