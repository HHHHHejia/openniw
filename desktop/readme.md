# OpenNIW desktop

A window around the two things you would otherwise run by hand: **your own
coding agent** and **the local companion's pages**. It removes the terminal,
not the architecture.

```
┌──────────────────────────────────────────────────────────┐
│ OpenNIW                                  [case folder ▾] │
├──────────────────────────────────────────────────────────┤
│ ①Evaluate ─ ②Frame ─ ③Evidence ─ ④Draft ─ ⑤Forms ─ ⑥Package│  ← live from STATE.md
├────────────────────────┬─────────────────────────────────┤
│                        │                                 │
│  your agent, running   │  the companion page the agent    │
│  in the case folder    │  just opened (127.0.0.1 only)   │
│  (a real terminal)     │                                 │
│                        │                                 │
└────────────────────────┴─────────────────────────────────┘
```

## What it does not do

This is the important part, and it should stay true of every future change:

- **It never touches an AI credential.** It spawns the `claude` or `codex`
  binary already installed on the machine; that CLI authenticates itself
  exactly as it does in a terminal. Nothing is read, stored, forwarded or
  proxied. (Anthropic's terms forbid using consumer-subscription OAuth
  tokens in third-party tools *including the Agent SDK* — spawning the real
  CLI is not that, and this app must never become that.)
- **It runs no server and holds no data.** The only listener is the
  companion's own 127.0.0.1 server, started by the agent in the user's case
  folder. The embedded view is hard-limited to loopback in `main.js`.
- **It is not a hosted service.** Same legal posture as the CLI: published
  software the user runs on their own machine, on their own files.

## How the two panes connect

**The sentinel is the source of truth**, not the agent's output. The
companion maintains `<case>/.openniw/ui-session.json` for every browser
step; `main.js` watches it and mirrors it into the right pane. Output
scraping for `OPENNIW_URL=` is kept as a fast path, but it cannot be the
mechanism, because:

- the agent may report a session it merely *found* with `openniw status`,
  having never re-run `ui` — so the line is never printed at all;
- the agent is a redrawing TUI, and a repainted or wrapped line defeats any
  regex over the PTY stream;
- a session that was left running before the app opened has no output to
  scrape in the first place.

Two rules that fall out of watching it, both learned the hard way:

- **Re-evaluate on a clock, not only on file events.** When the companion's
  server dies without finalizing, *nothing is written* — the sentinel reads
  `"running"` forever and only the stopped heartbeat gives it away. A
  file-change watcher alone would leave a dead page on screen indefinitely,
  so `watchCase()` also re-checks every five seconds.
- **Trust the heartbeat and the pid, not the status field.** A sentinel is
  live only if `status === "running"`, its heartbeat is under 90s old, and
  its pid still exists.

The Python side needed one small change: honouring `OPENNIW_NO_BROWSER=1`
so it does not *also* pop a system browser (`src/openniw/server.py`,
`src/openniw/cli.py`). The sentinel protocol and the pages are untouched.

The stepper reads `STATE.md` from the case folder every few seconds and
parses the same checklist the browser pages parse.

### Nobody gets sent to a browser that isn't there

The agent used to improvise "open this in your browser", which is wrong
inside this window — the page is already on screen beside it. Only the
companion knows where its page went, so the companion says it: the app sets
`OPENNIW_HOST=desktop` in the agent's environment, `openniw ui` prints a
ready-to-relay `SAY:` line worded for that host, and all four skills are
instructed to relay it verbatim instead of inventing their own. Terminal
users still get the address and the paste-it-yourself fallback.
`tests/test_ui_host.py` pins both halves of that contract.

## Two things the window tells the user that a terminal never would

**The skill command.** Skills are invoked by name and the prefix differs by
agent — `/niw-petition` in Claude Code, `$niw-petition` in Codex — which no
first-time user can guess. The command sits beside the running indicator and
types itself into the agent on click (typed, not sent, so the user can still
read it and add context). The `▾` lists all four skills.

**The statistical evaluation.** The page that answers "is this even worth
doing?" is reachable before a case folder exists: a prominent button on the
setup screen and a quiet one in the title bar. It is the same static export
as openniw.com/eval, **bundled into the app** and served over a private
`openniw://` scheme — so it works with no network, no companion and no case,
and its absolute asset paths still resolve. Escape or Close returns to the
window. Populate it with `make desktop-eval`; running from the repo the app
falls back to `webpage/out/`, and the button hides itself if neither exists.

## Layout

The chat pane can sit on the **left**, the **right**, or along the
**bottom** (the three buttons in the title bar: ◧ ◨ ⬓). One DOM order drives
all three — `#panes` just switches `flex-direction` between `row`,
`row-reverse` and `column-reverse` — so there is no duplicated markup and
the divider stays between the panes in every mode. The chosen layout and
both split sizes (one for the side layouts, one for the bottom) persist in
`localStorage`. Double-click the divider to reset the split.

## Run it

```bash
cd desktop
npm install
npm start          # npm run dev for devtools
```

Requirements on the user's machine:

| | why |
|---|---|
| `claude` or `codex`, logged in | the AI. Yours, not ours. |
| Python 3 | only for the companion's form pages |
| `openniw` | installed by the agent on first use; not needed up front |

`npm run dist` produces an unpacked app; `npm run pack` builds a DMG /
NSIS / AppImage via electron-builder.

## Layout

```
desktop/
├── main.js               # window, PTY spawn, OPENNIW_URL watch, loopback lock
├── preload.js            # the entire renderer↔machine surface (contextBridge)
└── renderer/
    ├── index.html        # setup gate + two panes
    ├── renderer.js       # xterm wiring, stepper, page pane, split
    └── styles.css        # the docket look, matching the web UI
```

## Notes for maintainers

- `node-pty` must be **1.2.0-beta or newer**: 1.1.0's prebuild fails with
  `posix_spawnp failed` on current Node/Electron. It ships N-API prebuilds,
  so no native rebuild step is needed.
- macOS GUI apps inherit a stunted `PATH`; `loginPath()` in `main.js` asks
  the login shell for the real one, which is why `claude` is found at all.
- The renderer builds some markup with `innerHTML`; every interpolated
  value goes through `escapeHtml` first, including filesystem paths.
- **Do not simplify the divider drag.** The page pane is an out-of-process
  `<webview>`: the moment the pointer crosses into it, the parent document
  stops receiving `pointermove`, which strands the drag (it could be pulled
  one way but never back). `#dragShield` covers the whole viewport while
  dragging so every event stays in this document, and the resize is
  committed once per `requestAnimationFrame` — re-laying out the embedded
  view on every pointer event is what made it crawl. Pointer capture is not
  a substitute; it is not dependable across the process boundary.
- `backgroundThrottling: false` is deliberate: a minimized window must not
  stall the terminal while the agent is still working.
- Keep the setup gate honest: it tells the user plainly that the app runs
  their agent under their subscription and that OpenNIW is not a law firm.
