/* Renderer: two panes over one idea.
   Left  — a real terminal running the user's own agent CLI.
   Right — whatever localhost page that agent's companion just opened.
   The bridge between them is one line the companion already prints:
   OPENNIW_URL=… (see main.js). */

const $ = (id) => document.getElementById(id);

const state = {
  agent: "claude",
  caseDir: null,
  running: false,
  lastUrl: null,
  statePoll: null,
};

// ------------------------------------------------------------- terminal

const term = new Terminal({
  fontFamily: '"IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace',
  fontSize: 13,
  lineHeight: 1.25,
  cursorBlink: true,
  allowProposedApi: true,
  theme: {
    background: "#1a1a17",
    foreground: "#e8e6df",
    cursor: "#1f6f54",
    selectionBackground: "#33413a",
    black: "#1a1a17", red: "#c05621", green: "#1f8a5f", yellow: "#b7791f",
    blue: "#2b6cb0", magenta: "#805ad5", cyan: "#2c7a7b", white: "#e8e6df",
  },
});
const fit = new FitAddon.FitAddon();
term.loadAddon(fit);
term.open($("term"));

function refit() {
  try {
    fit.fit();
    if (state.running) window.openniw.resize(term.cols, term.rows);
  } catch { /* pane hidden or zero-sized */ }
}
new ResizeObserver(refit).observe($("termWrap"));
window.addEventListener("resize", refit);

term.onData((d) => { if (state.running) window.openniw.sendInput(d); });

window.openniw.onAgentData((d) => term.write(d));
window.openniw.onAgentExit((code) => {
  state.running = false;
  setAgentState(`exited (${code})`, false);
  $("restartBtn").hidden = false;
  term.writeln(`\r\n\x1b[2m— agent exited (${code}). Your case folder is untouched; press Restart to continue. —\x1b[0m`);
});

// ------------------------------------------------- companion page pane

window.openniw.onCompanionUrl((url) => showPage(url));
window.openniw.onCompanionClosed(() => clearPage());

function showPage(url) {
  if (url === state.lastUrl) return;
  state.lastUrl = url;
  const view = $("view");
  view.hidden = false;
  $("placeholder").hidden = true;
  view.src = url;

  const step = (url.match(/127\.0\.0\.1:\d+\/([a-z-]+)\//) || [])[1] || "page";
  $("pageTitle").textContent = step.charAt(0).toUpperCase() + step.slice(1);
  const pill = $("pageUrl");
  pill.textContent = url.replace(/\?token=.*/, "");
  pill.hidden = false;
  pill.classList.add("live");
  $("reloadBtn").hidden = false;
  $("popOutBtn").hidden = false;
}

function clearPage() {
  if (!state.lastUrl) return;
  state.lastUrl = null;
  const view = $("view");
  view.hidden = true;
  view.src = "about:blank";
  $("placeholder").hidden = false;
  $("pageTitle").textContent = "Browser step";
  $("pageUrl").hidden = true;
  $("reloadBtn").hidden = true;
  $("popOutBtn").hidden = true;
}

$("reloadBtn").onclick = () => { const v = $("view"); if (v.src) v.reload(); };
$("popOutBtn").onclick = () => {
  if (state.lastUrl) window.openniw.openExternal(state.lastUrl);
};

// ---------------------------------------------------------- the stepper

// Same contract the browser pages use: the agent keeps a six- (or seven-)
// line checklist in STATE.md, and the marker "←" names the current stage.
const STAGE_RE = /^\s*-\s*\[( |x|X)\]\s+(I{1,3}V?|IV|V|R)(·[ab])?\s+(\S+)/;

function renderStepper(md) {
  const el = $("stepper");
  if (!md) { el.hidden = true; document.body.classList.remove("has-stepper"); return; }

  const rows = [];
  let sawCurrent = false;
  for (const line of md.split("\n")) {
    const m = line.match(STAGE_RE);
    if (!m) continue;
    const id = m[2] + (m[3] || "");
    if (rows.some((r) => r.id === id)) continue;
    let status = "todo";
    if (m[1].toLowerCase() === "x") status = "done";
    else if (!sawCurrent && (line.includes("←") || line.includes("<-"))) {
      status = "current"; sawCurrent = true;
    }
    rows.push({ id, label: m[4], status });
  }
  if (!rows.length) { el.hidden = true; document.body.classList.remove("has-stepper"); return; }
  if (!sawCurrent) {
    const first = rows.find((r) => r.status === "todo");
    if (first) first.status = "current";
  }

  el.innerHTML = rows.map((r, i) => `
    <div class="stage ${r.status}">
      <div class="dot">${r.status === "done" ? "✓" : r.id.replace("·", "")}</div>
      <div class="lbl">${r.id} ${escapeHtml(r.label)}</div>
      ${i < rows.length - 1 ? '<div class="bar"></div>' : ""}
    </div>`).join("");
  el.hidden = false;
  document.body.classList.add("has-stepper");
  refit();
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

async function pollState() {
  if (!state.caseDir) return;
  renderStepper(await window.openniw.readState(state.caseDir));
}

// -------------------------------------------------------------- setup

// Paths come off the filesystem, so they go through escapeHtml like any
// other untrusted string before they reach innerHTML.
const CHECK_COPY = {
  agent: {
    what: (m) => `${escapeHtml(m.label)} installed`,
    okWhy: (m) => `Found at <code>${escapeHtml(m.path)}</code>. It signs in as itself — this app never sees your subscription or any token.`,
    badWhy: (m) => `Not on PATH. Install it, sign in once, then re-check: <code>${escapeHtml(m.installHint)}</code> · <a href="#" data-ext="${escapeHtml(m.install)}">docs</a>`,
  },
  python: {
    what: () => "Python 3",
    okWhy: (m) => `Found at <code>${escapeHtml(m.path)}</code>. Needed only for the local form pages.`,
    badWhy: () => `Not found. macOS: <code>brew install python</code>. Without it the chat still works; the browser steps will not.`,
  },
  openniw: {
    what: () => "openniw companion",
    okWhy: (m) => `Found at <code>${escapeHtml(m.path)}</code>.`,
    badWhy: () => `Not installed yet — that is fine. Your agent installs it the first time a step needs it (<code>uv tool install openniw</code>).`,
  },
};

let detected = null;

async function runChecks() {
  detected = await window.openniw.detect();

  const sel = $("agentSel");
  sel.innerHTML = Object.entries(detected)
    .filter(([k]) => k === "claude" || k === "codex")
    .map(([k, m]) => `<option value="${k}" ${m.path ? "" : "disabled"}>${m.label}${m.path ? "" : " — not installed"}</option>`)
    .join("");
  const firstReady = ["claude", "codex"].find((k) => detected[k].path);
  state.agent = firstReady || "claude";
  sel.value = state.agent;

  const items = [];
  for (const key of ["claude", "codex"]) {
    const m = detected[key];
    if (!m.path && firstReady && key !== firstReady) continue;  // don't nag about the other one
    items.push(row(m.path, CHECK_COPY.agent, m));
  }
  items.push(row(detected.python.path, CHECK_COPY.python, detected.python));
  items.push(row(detected.openniw.path, CHECK_COPY.openniw, detected.openniw, true));
  if (!detected.ptyReady) {
    items.push(`<li class="bad"><span class="mark">!</span><div><div class="what">Terminal bridge not built</div>
      <div class="why">node-pty did not load for this Electron build. In <code>desktop/</code> run <code>npm rebuild node-pty</code> (or <code>npx electron-rebuild</code>).</div></div></li>`);
  }
  $("checks").innerHTML = items.join("");

  $("checks").querySelectorAll("[data-ext]").forEach((a) => {
    a.onclick = (e) => { e.preventDefault(); window.openniw.openExternal(a.dataset.ext); };
  });

  $("beginBtn").disabled = !firstReady || !detected.ptyReady;

  const recents = await window.openniw.recentCases();
  if (recents.length) {
    $("recents").hidden = false;
    $("recentList").innerHTML = recents.map((r) => `
      <li><button data-dir="${escapeHtml(r.dir)}">
        <b>${escapeHtml(r.name)}</b>${r.hasState ? " · in progress" : " · new"}
        <div class="path">${escapeHtml(r.dir)}</div>
      </button></li>`).join("");
    $("recentList").querySelectorAll("button").forEach((b) => {
      b.onclick = () => begin(b.dataset.dir);
    });
  }
}

function row(ok, copy, meta, optional = false) {
  const cls = ok ? "ok" : (optional ? "" : "bad");
  return `<li class="${cls}"><span class="mark">${ok ? "✓" : (optional ? "·" : "!")}</span>
    <div><div class="what">${copy.what(meta)}</div>
    <div class="why">${ok ? copy.okWhy(meta) : copy.badWhy(meta)}</div></div></li>`;
}

// ------------------------------------------------------ skill hint chip

// The skills are invoked by name, and the prefix differs per agent —
// Claude Code takes /skill-name, Codex takes $skill-name. New users have no
// way to guess that, so the command sits next to the running indicator and
// types itself into the terminal on click.
const SKILLS = [
  ["niw-petition", "EB-2 NIW self-petition"],
  ["eb1a-petition", "EB-1A extraordinary ability"],
  ["o1-petition", "O-1A petition kit"],
  ["i485-adjustment", "I-485 adjustment of status"],
];

const skillPrefix = () => (state.agent === "codex" ? "$" : "/");

function renderSkillHint() {
  const p = skillPrefix();
  $("skillCmd").textContent = p + SKILLS[0][0];
  $("skillMenu").innerHTML = SKILLS.map(([name, desc]) => `
    <button data-cmd="${escapeHtml(p + name)}">
      <div class="cmd">${escapeHtml(p + name)}</div>
      <div class="desc">${escapeHtml(desc)}</div>
    </button>`).join("");
  $("skillMenu").querySelectorAll("button").forEach((b) => {
    b.onclick = () => { typeSkill(b.dataset.cmd); $("skillMenu").hidden = true; };
  });
  $("skillHint").hidden = false;
}

function typeSkill(cmd) {
  if (!state.running) return;
  // Type it, do not send it: the user still gets to read it and add context
  // before pressing Enter.
  window.openniw.sendInput(cmd);
  term.focus();
  const chip = $("skillCmd");
  chip.classList.add("copied");
  setTimeout(() => chip.classList.remove("copied"), 700);
}

$("skillCmd").onclick = () => typeSkill($("skillCmd").textContent);
$("skillMore").onclick = (e) => {
  e.stopPropagation();
  const m = $("skillMenu");
  m.hidden = !m.hidden;
};
document.addEventListener("click", (e) => {
  if (!$("skillHint").contains(e.target)) $("skillMenu").hidden = true;
});

// ------------------------------------------- statistical evaluation panel

// Worth seeing before a case folder exists — it is the honest first answer
// to "is this even worth doing?". Served from inside the app, so it works
// with no network and no companion running.
const evalPanel = { url: null, loaded: false };

async function initEval() {
  // The button is ALWAYS shown. Hiding it when the bundle is missing made
  // the feature invisible and the failure silent — the two worst outcomes.
  $("evalBtn").hidden = false;
  $("evalBtnBar").hidden = false;
  try {
    const info = await window.openniw.evalInfo();
    evalPanel.url = info.available ? info.url : null;
  } catch (err) {
    evalPanel.url = null;
    evalPanel.error = String(err && err.message || err);
  }
}

function evalFailure(detail) {
  $("evalView").hidden = true;
  let box = $("evalMissing");
  if (!box) {
    box = document.createElement("div");
    box.id = "evalMissing";
    $("evalPanel").appendChild(box);
  }
  box.hidden = false;
  box.innerHTML = `
    <p class="ph-title">The evaluation page is not in this build</p>
    <p class="ph-body">${escapeHtml(detail)}</p>
    <p class="ph-body">Rebuild it from the repo root:</p>
    <pre class="evalFix">make desktop-eval</pre>
    <p class="ph-body">Or open the same page online at
      <a href="#" id="evalOnline">openniw.com/eval</a>.</p>`;
  const link = $("evalOnline");
  if (link) link.onclick = (e) => {
    e.preventDefault();
    window.openniw.openExternal("https://openniw.com/eval/");
  };
}

function openEval() {
  $("evalPanel").hidden = false;
  if (!evalPanel.url) {
    evalFailure(evalPanel.error
      || "desktop/eval/ is missing, and webpage/out/ was not found either.");
    return;
  }
  const box = $("evalMissing");
  if (box) box.hidden = true;
  const view = $("evalView");
  view.hidden = false;
  if (!evalPanel.loaded) {
    evalPanel.loaded = true;
    view.addEventListener("did-fail-load", (e) => {
      if (e.errorCode === -3) return;   // aborted, not a real failure
      evalPanel.loaded = false;
      evalFailure(`The page failed to load (${e.errorDescription || e.errorCode}).`);
    });
    view.src = evalPanel.url;
  }
}
function closeEval() { $("evalPanel").hidden = true; }

$("evalBtn").onclick = openEval;
$("evalBtnBar").onclick = openEval;
$("evalClose").onclick = closeEval;
window.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && !$("evalPanel").hidden) closeEval();
});

$("recheckBtn").onclick = runChecks;
$("agentSel").onchange = (e) => { state.agent = e.target.value; };

$("beginBtn").onclick = async () => {
  const info = await window.openniw.pickCase();
  if (info) begin(info.dir, info);
};
$("caseBtn").onclick = async () => {
  const info = await window.openniw.pickCase();
  if (info) begin(info.dir, info);
};
$("revealBtn").onclick = () => window.openniw.revealCase(state.caseDir);
$("restartBtn").onclick = () => start();

async function begin(dir, info) {
  info = info || await window.openniw.describeCase(dir);
  if (!info) return;

  // The CLI refuses to run from a parent that merely CONTAINS a case folder;
  // catch that here so the user fixes it before the agent complains.
  if (!info.hasState && info.nestedCase) {
    const go = confirm(
      `"${info.name}" is not a case folder, but it contains one: ${info.nestedCase}.\n\n` +
      `Open ${info.nestedCase} instead?`);
    if (go) return begin(dir + "/" + info.nestedCase);
  }

  state.caseDir = info.dir;
  $("setup").hidden = true;
  $("caseName").textContent = info.name;
  $("revealBtn").hidden = false;
  // Watch the sentinel before the agent even starts: a session left running
  // from an earlier sitting should reappear in the pane immediately.
  await window.openniw.watchCase(info.dir);
  await start();
  await pollState();
  clearInterval(state.statePoll);
  state.statePoll = setInterval(pollState, 4000);
}

async function start() {
  refit();
  const r = await window.openniw.startAgent({
    agent: state.agent, cwd: state.caseDir, cols: term.cols, rows: term.rows,
  });
  if (!r.ok) {
    term.writeln(`\r\n\x1b[31m${r.error}\x1b[0m\r\n`);
    setAgentState("failed", false);
    return;
  }
  state.running = true;
  $("agentLabel").textContent = r.label;
  $("restartBtn").hidden = true;
  setAgentState("running", true);
  renderSkillHint();
  term.focus();
}

function setAgentState(text, live) {
  const el = $("agentState");
  el.textContent = text;
  el.classList.toggle("live", !!live);
}

// --------------------------------------------------- layout + split drag

const LAYOUTS = ["left", "right", "bottom"];
const layout = {
  mode: localStorage.getItem("openniw.layout") || "left",
  size: Number(localStorage.getItem("openniw.chatSize")) || 46,   // side: width %
  sizeV: Number(localStorage.getItem("openniw.chatSizeV")) || 42, // bottom: height %
};

function applyLayout(persist = true) {
  const panes = $("panes");
  panes.classList.remove("lay-left", "lay-right", "lay-bottom");
  panes.classList.add("lay-" + layout.mode);
  panes.style.setProperty("--chat-size", layout.size + "%");
  panes.style.setProperty("--chat-size-v", layout.sizeV + "%");
  document.querySelectorAll("#layoutPick button").forEach((b) => {
    b.classList.toggle("on", b.dataset.layout === layout.mode);
  });
  if (persist) {
    localStorage.setItem("openniw.layout", layout.mode);
    localStorage.setItem("openniw.chatSize", String(layout.size));
    localStorage.setItem("openniw.chatSizeV", String(layout.sizeV));
  }
  refit();
}

document.querySelectorAll("#layoutPick button").forEach((b) => {
  b.onclick = () => {
    if (!LAYOUTS.includes(b.dataset.layout)) return;
    layout.mode = b.dataset.layout;
    applyLayout();
  };
});

(function splitter() {
  const bar = $("split");
  const shield = $("dragShield");
  let dragging = false;
  let frame = null;
  let pending = null;

  const vertical = () => layout.mode === "bottom";

  function commit() {
    frame = null;
    if (pending === null) return;
    const panes = $("panes");
    if (vertical()) {
      layout.sizeV = pending;
      panes.style.setProperty("--chat-size-v", pending + "%");
    } else {
      layout.size = pending;
      panes.style.setProperty("--chat-size", pending + "%");
    }
    pending = null;
  }

  function move(e) {
    if (!dragging) return;
    const r = $("panes").getBoundingClientRect();
    let pct;
    if (vertical()) {
      // chat sits at the bottom: its height grows as the pointer goes up
      pct = ((r.bottom - e.clientY) / r.height) * 100;
    } else if (layout.mode === "right") {
      pct = ((r.right - e.clientX) / r.width) * 100;
    } else {
      pct = ((e.clientX - r.left) / r.width) * 100;
    }
    pending = Math.min(80, Math.max(18, pct));
    // One layout write per frame: the page pane is an out-of-process view
    // and re-laying it out on every pointer event is what made this crawl.
    if (frame === null) frame = requestAnimationFrame(commit);
  }

  function stop() {
    if (!dragging) return;
    dragging = false;
    if (frame !== null) { cancelAnimationFrame(frame); commit(); }
    shield.hidden = true;
    shield.classList.remove("col", "row");
    bar.classList.remove("dragging");
    applyLayout();          // persists the new size and refits the terminal
  }

  bar.addEventListener("pointerdown", (e) => {
    dragging = true;
    bar.classList.add("dragging");
    // Raise the shield BEFORE the pointer can travel: once it is up, every
    // pointer event lands on an element in this document and reaches the
    // window listeners below, whichever pane the cursor is over.
    shield.hidden = false;
    shield.classList.add(vertical() ? "row" : "col");
    e.preventDefault();
  });
  // On window, not on the divider: pointer capture is not dependable across
  // the out-of-process page view, but the shield guarantees delivery here.
  window.addEventListener("pointermove", move);
  window.addEventListener("pointerup", stop);
  window.addEventListener("pointercancel", stop);
  window.addEventListener("blur", stop);
  // double-click the divider to reset to the default split
  bar.addEventListener("dblclick", () => {
    if (vertical()) layout.sizeV = 42; else layout.size = 46;
    applyLayout();
  });
})();

applyLayout(false);
initEval();
runChecks();
