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
  `python3 -m pip install --user openniw` — the companion, from **PyPI**:
  <https://pypi.org/project/openniw/>. The skills do not install from a
  GitHub URL; if you ever see one instructed, treat it as a red flag;
- `pip install pypdf cryptography` — only for the offline PDF-filling
  fallback.

The optional desktop window is **not** installed by any skill. If you ask
for it, the agent points you at the readme and you run the two commands
yourself.

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

## Published audit findings and what was done

The skills are scanned by [skills.sh](https://www.skills.sh/hhhhhejia/openniw).
Every finding raised so far is listed here with its outcome, because a risk
rating with no explanation is not information.

| Finding | Verdict | Action |
|---|---|---|
| **E005 — Suspicious download URL** (installing from a personal GitHub account) | **Valid.** A skill that tells an agent to fetch and run code from an individual's repository is shaped exactly like a supply-chain attack, and no reader can tell the difference from the text. | Fixed. `openniw` is published on [PyPI](https://pypi.org/project/openniw/) and the GitHub fallback is deleted from all four skills. The desktop window is no longer installed by any skill either. Pinned by `tests/test_ui_host.py`. |
| **W007 — Insecure credential handling** (the page URL carried a session token the agent had to speak) | **Valid.** That token authorises a server holding the entire case, and relaying it copied it into the model's context and every transcript downstream. | Fixed. The URL is no longer printed to the agent at all: hosts read it from the session file, humans use `openniw open`. No host's wording contains a token, asserted for all three. |
| **W011 — Third-party content exposure** (indirect prompt injection through uploaded documents) | **Valid and inherent.** The product's job is to read CVs, notices and web pages, which are attacker-controllable text. | Mitigated. All four skills now state, beside the standing rules, that documents are data and never instructions; embedded commands are ignored and reported to you rather than acted on. |

Scanners also flag these skills for handling sensitive personal
identifiers. That one is true and cannot be designed away: preparing an
I-485 requires an A-Number and a passport number. The mitigation is not to
hide it but to keep it local and auditable, which is what this page and the
rest of this repository are for.

If a scan reports something this page does not explain, please open an
issue. That would be a real finding and it will be fixed.
