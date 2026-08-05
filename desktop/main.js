// OpenNIW desktop shell.
//
// What this is: a window that runs the SAME two things you would otherwise
// run by hand — your own coding agent (the `claude` or `codex` CLI already
// installed and logged in on this machine) and the `openniw` companion's
// localhost pages. It launches them; it does not replace them.
//
// What it deliberately does NOT do, and must never do:
//   · read, store, forward or proxy any AI credential. The agent CLI
//     authenticates itself exactly as it does in a terminal. Anthropic's
//     terms forbid using consumer-subscription OAuth tokens in third-party
//     tools (including the Agent SDK); spawning the real CLI is not that,
//     and this file must keep it that way.
//   · send anything anywhere. The only network listener is the companion's
//     own 127.0.0.1 server, started by the agent, not by us.
//   · touch the case folder. The agent and the companion own it.

const { app, BrowserWindow, ipcMain, dialog, shell, session, protocol, net } = require("electron");
const path = require("path");
const fs = require("fs");
const os = require("os");
const { execFile } = require("child_process");

let pty = null;
try {
  pty = require("node-pty");
} catch (err) {
  // Surfaced in the UI as a setup error rather than crashing on boot.
  console.error("node-pty unavailable:", err.message);
}

/* The statistical evaluation is the one page worth seeing before a case
   even exists, so it ships INSIDE the app rather than being fetched: the
   same static export as openniw.com/eval, served from a private scheme so
   its absolute asset paths (/_next/…, /benchmark-data.json) resolve without
   a server and without a single network request. Populate with
   `make desktop-eval`; the button hides itself if it is missing. */
const EVAL_SCHEME = "openniw";
const EVAL_ROOTS = [
  path.join(__dirname, "eval"),                       // packaged / synced
  path.join(__dirname, "..", "webpage", "out"),       // running from the repo
];
function evalRoot() {
  return EVAL_ROOTS.find((p) => fs.existsSync(path.join(p, "eval", "index.html"))) || null;
}

protocol.registerSchemesAsPrivileged([{
  scheme: EVAL_SCHEME,
  privileges: { standard: true, secure: true, supportFetchAPI: true },
}]);

const AGENTS = {
  claude: {
    label: "Claude Code",
    bin: "claude",
    install: "https://claude.com/claude-code",
    installHint: "npm install -g @anthropic-ai/claude-code",
  },
  codex: {
    label: "Codex",
    bin: "codex",
    install: "https://developers.openai.com/codex/cli",
    installHint: "npm install -g @openai/codex",
  },
};

/** PATH as a login shell would see it — GUI apps on macOS inherit a stunted
 *  PATH, which is the classic "works in Terminal, not in the app" bug. */
let cachedPath = null;
function loginPath() {
  if (cachedPath) return cachedPath;
  cachedPath = process.env.PATH || "";
  if (process.platform === "win32") return cachedPath;
  try {
    const shellBin = process.env.SHELL || "/bin/zsh";
    const out = require("child_process")
      .execFileSync(shellBin, ["-ilc", "printf %s \"$PATH\""], {
        encoding: "utf8", timeout: 5000, stdio: ["ignore", "pipe", "ignore"],
      })
      .trim();
    if (out) cachedPath = out;
  } catch {
    // keep the inherited PATH; which() will report what is missing
  }
  const extra = [
    "/opt/homebrew/bin", "/usr/local/bin",
    path.join(os.homedir(), ".local", "bin"),
    path.join(os.homedir(), ".bun", "bin"),
  ].filter((p) => fs.existsSync(p) && !cachedPath.split(":").includes(p));
  if (extra.length) cachedPath = [...extra, cachedPath].join(":");
  return cachedPath;
}

function childEnv(extra = {}) {
  return {
    ...process.env,
    PATH: loginPath(),
    // Tell the companion where its pages actually appear: it prints the
    // sentence the agent relays, and skips popping a system browser.
    OPENNIW_HOST: "desktop",
    OPENNIW_NO_BROWSER: "1",
    TERM: "xterm-256color",
    ...extra,
  };
}

function which(bin) {
  return new Promise((resolve) => {
    const finder = process.platform === "win32" ? "where" : "which";
    execFile(finder, [bin], { env: childEnv() }, (err, stdout) => {
      resolve(err ? null : stdout.split(/\r?\n/)[0].trim() || null);
    });
  });
}

// ---------------------------------------------------------------- window

let win = null;

function createWindow() {
  win = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 960,
    minHeight: 600,
    title: "OpenNIW",
    backgroundColor: "#faf9f5",
    titleBarStyle: process.platform === "darwin" ? "hiddenInset" : "default",
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false, // preload needs require() for the IPC bridge
      webviewTag: true,
      // A minimized window must not stall the terminal: the agent keeps
      // streaming whether or not anyone is looking at it.
      backgroundThrottling: false,
    },
  });
  win.loadFile(path.join(__dirname, "renderer", "index.html"));
  if (process.argv.includes("--dev")) win.webContents.openDevTools({ mode: "detach" });

  // Anything that is not our own UI or the local companion opens in the
  // user's real browser instead of inside the app.
  win.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: "deny" };
  });
}

app.whenReady().then(() => {
  // Serve the bundled evaluation page. Everything is resolved inside the
  // root directory; anything that climbs out gets a 403 rather than a file.
  protocol.handle(EVAL_SCHEME, async (request) => {
    const root = evalRoot();
    if (!root) return new Response("evaluation page not installed", { status: 404 });
    let rel;
    try { rel = decodeURIComponent(new URL(request.url).pathname); }
    catch { return new Response("bad path", { status: 400 }); }
    let file = path.normalize(path.join(root, rel));
    if (!file.startsWith(path.normalize(root))) {
      return new Response("forbidden", { status: 403 });
    }
    try {
      if (fs.statSync(file).isDirectory()) file = path.join(file, "index.html");
    } catch { /* fall through to the read error below */ }
    try {
      return await net.fetch("file://" + file);
    } catch {
      return new Response("not found", { status: 404 });
    }
  });

  // Guests (the embedded page views) may not wander: local origins only,
  // and anything that wants a new window goes to the real browser.
  app.on("web-contents-created", (_e, contents) => {
    contents.setWindowOpenHandler(({ url }) => {
      if (/^https?:\/\//.test(url)) shell.openExternal(url);
      return { action: "deny" };
    });
    contents.on("will-navigate", (evt, url) => {
      let ok = false;
      try {
        const u = new URL(url);
        ok = u.protocol === `${EVAL_SCHEME}:` || u.protocol === "file:"
          || ["127.0.0.1", "localhost", "::1"].includes(u.hostname);
      } catch { /* malformed — refuse */ }
      if (!ok) { evt.preventDefault(); shell.openExternal(url); }
    });
  });

  // The embedded view may only ever reach loopback. A page that tried to
  // call out would be a bug worth failing loudly on.
  session.defaultSession.webRequest.onBeforeRequest(
    { urls: ["http://*/*", "https://*/*"] },
    (details, callback) => {
      let host = "";
      try { host = new URL(details.url).hostname; } catch { /* ignore */ }
      const loopback = host === "127.0.0.1" || host === "localhost" || host === "::1";
      callback({ cancel: !loopback });
    },
  );

  createWindow();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  killAgent();
  if (process.platform !== "darwin") app.quit();
});
app.on("before-quit", killAgent);

// ------------------------------------------------------------ agent term

let term = null;
let termAgent = null;

function killAgent() {
  if (!term) return;
  try { term.kill(); } catch { /* already gone */ }
  term = null;
  termAgent = null;
}

/** The companion prints `OPENNIW_URL=http://127.0.0.1:PORT/step/?token=…`
 *  when a browser step starts. That single line is the whole integration:
 *  we watch the agent's output for it and load the page in the right pane.
 *  Nothing in the Python side had to change to make this work. */
const URL_RE = /OPENNIW_URL=(http:\/\/127\.0\.0\.1:\d+\/[^\s\x1b]*)/g;

// Terminal escape sequences can split a line across chunks; keep a tail.
let urlTail = "";
function scanForUrl(chunk) {
  const hay = urlTail + chunk;
  let last = null;
  let m;
  URL_RE.lastIndex = 0;
  while ((m = URL_RE.exec(hay)) !== null) last = m[1];
  urlTail = hay.slice(-400);
  return last;
}

ipcMain.handle("agent:detect", async () => {
  const out = {};
  for (const [key, meta] of Object.entries(AGENTS)) {
    out[key] = { ...meta, path: await which(meta.bin) };
  }
  out.python = { path: (await which("python3")) || (await which("python")) };
  out.openniw = { path: await which("openniw") };
  out.ptyReady = !!pty;
  return out;
});

ipcMain.handle("agent:start", async (_evt, { agent, cwd, cols, rows }) => {
  if (!pty) return { ok: false, error: "node-pty is not built for this Electron version. Run `npm rebuild` in desktop/." };
  const meta = AGENTS[agent];
  if (!meta) return { ok: false, error: `unknown agent: ${agent}` };
  const bin = await which(meta.bin);
  if (!bin) return { ok: false, error: `${meta.label} is not installed or not on PATH.` };
  if (!cwd || !fs.existsSync(cwd)) return { ok: false, error: "pick a case folder first" };

  killAgent();
  urlTail = "";
  term = pty.spawn(bin, [], {
    name: "xterm-color",
    cols: cols || 100,
    rows: rows || 30,
    cwd,
    env: childEnv(),
  });
  termAgent = agent;

  term.onData((data) => {
    if (!win || win.isDestroyed()) return;
    win.webContents.send("agent:data", data);
    const url = scanForUrl(data);
    if (url) win.webContents.send("companion:url", url);
  });
  term.onExit(({ exitCode }) => {
    if (win && !win.isDestroyed()) win.webContents.send("agent:exit", exitCode);
    term = null;
    termAgent = null;
  });

  return { ok: true, bin, agent, label: meta.label };
});

ipcMain.on("agent:input", (_evt, data) => {
  if (term) term.write(data);
});

ipcMain.on("agent:resize", (_evt, { cols, rows }) => {
  if (term) { try { term.resize(cols, rows); } catch { /* race with exit */ } }
});

ipcMain.handle("agent:stop", () => { killAgent(); return { ok: true }; });

// ------------------------------------------------------------ case folder

const RECENTS = path.join(app.getPath("userData"), "recent-cases.json");

function readRecents() {
  try { return JSON.parse(fs.readFileSync(RECENTS, "utf8")); } catch { return []; }
}
function writeRecents(list) {
  try {
    fs.mkdirSync(path.dirname(RECENTS), { recursive: true });
    fs.writeFileSync(RECENTS, JSON.stringify(list.slice(0, 8), null, 2));
  } catch { /* recents are a convenience, never a requirement */ }
}

/** A case folder is one that already holds STATE.md, or an empty-ish folder
 *  the agent is about to initialize. Mirrors the CLI's own guard so the two
 *  cannot disagree about what "the case folder" means. */
function describeCase(dir) {
  const has = (f) => fs.existsSync(path.join(dir, f));
  let nested = null;
  try {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.isDirectory() && fs.existsSync(path.join(dir, entry.name, "STATE.md"))) {
        nested = entry.name;
        break;
      }
    }
  } catch { /* unreadable dir */ }
  return {
    dir,
    name: path.basename(dir),
    hasState: has("STATE.md"),
    hasCaseJson: has("case.json"),
    nestedCase: nested,
    sentinel: has(path.join(".openniw", "ui-session.json")),
  };
}

// ------------------------------------------------------- session sentinel

/* Scraping the agent's output for OPENNIW_URL= is not enough on its own:
   the agent may report a session it found with `openniw status` (never
   re-running `ui`, so the line is never printed), and a redrawing TUI can
   wrap or repaint the line out of recognition. The sentinel the companion
   maintains in the case folder is the authoritative record of what is
   live, so that is what we watch. Output scraping stays as a fast path. */
const HEARTBEAT_STALE_MS = 90_000;
let watchedSentinel = null;
let sentinelTimer = null;
let lastSentinelUrl = null;

function sentinelPath(dir) {
  return path.join(dir, ".openniw", "ui-session.json");
}

function readSentinel(dir) {
  try {
    const s = JSON.parse(fs.readFileSync(sentinelPath(dir), "utf8"));
    if (!s || s.status !== "running" || !s.url) return null;
    const beat = Date.parse(s.heartbeat_at || s.started_at || 0);
    if (Number.isFinite(beat) && Date.now() - beat > HEARTBEAT_STALE_MS) {
      return null;                       // server died without finalizing
    }
    try { process.kill(s.pid, 0); } catch { return null; }  // pid is gone
    return s;
  } catch {
    return null;                         // absent or mid-write
  }
}

function pushSentinel(dir) {
  if (!win || win.isDestroyed()) return;
  const s = readSentinel(dir);
  const url = s ? s.url : null;
  if (url === lastSentinelUrl) return;
  lastSentinelUrl = url;
  if (url) win.webContents.send("companion:url", url);
  else win.webContents.send("companion:closed");
}

function watchCase(dir) {
  if (watchedSentinel) { fs.unwatchFile(watchedSentinel); watchedSentinel = null; }
  if (sentinelTimer) { clearInterval(sentinelTimer); sentinelTimer = null; }
  lastSentinelUrl = null;
  if (!dir) return;
  const file = sentinelPath(dir);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  // Polling rather than fs.watch: the file is written atomically via
  // rename, which fs.watch reports inconsistently across platforms.
  fs.watchFile(file, { interval: 1000 }, () => pushSentinel(dir));
  // A file event alone is not enough. When the server dies without
  // finalizing, NOTHING is written — the sentinel still reads "running"
  // forever and only the stopped heartbeat gives it away. Staleness is a
  // function of elapsed time, so it has to be re-evaluated on a clock.
  sentinelTimer = setInterval(() => pushSentinel(dir), 5000);
  watchedSentinel = file;
  pushSentinel(dir);                     // catch a session already running
}

ipcMain.handle("case:watch", (_evt, dir) => { watchCase(dir); return true; });

ipcMain.handle("case:pick", async () => {
  const r = await dialog.showOpenDialog(win, {
    title: "Choose or create your case folder",
    properties: ["openDirectory", "createDirectory"],
    buttonLabel: "Use this folder",
  });
  if (r.canceled || !r.filePaths[0]) return null;
  const info = describeCase(r.filePaths[0]);
  const recents = readRecents().filter((p) => p !== info.dir);
  writeRecents([info.dir, ...recents]);
  return info;
});

ipcMain.handle("case:recents", () =>
  readRecents().filter((p) => fs.existsSync(p)).map(describeCase));

ipcMain.handle("case:describe", (_evt, dir) =>
  (dir && fs.existsSync(dir) ? describeCase(dir) : null));

ipcMain.handle("case:reveal", (_evt, dir) => {
  if (dir && fs.existsSync(dir)) shell.openPath(dir);
  return true;
});

ipcMain.handle("case:state", (_evt, dir) => {
  try { return fs.readFileSync(path.join(dir, "STATE.md"), "utf8"); }
  catch { return null; }
});

ipcMain.handle("eval:info", () => ({
  available: !!evalRoot(),
  url: `${EVAL_SCHEME}://local/eval/`,
}));

ipcMain.handle("open:external", (_evt, url) => {
  if (/^https?:\/\//.test(url)) shell.openExternal(url);
  return true;
});
