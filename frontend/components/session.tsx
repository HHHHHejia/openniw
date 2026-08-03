"use client";
import { useEffect, useState } from "react";
import { api, withToken } from "@/lib/api";

// The global journey stepper. Stage statuses are parsed live from the
// case's STATE.md (the agent maintains it); stages with a browser page
// link to it, chat-only stages say so.

type StageId = "I" | "II·a" | "II·b" | "III" | "IV" | "V" | "R";
type StageStatus = "done" | "current" | "todo";

// "R" (RFE response) is a conditional stage: it renders only when the
// agent has appended an R line to STATE.md's checklist (RFE mode active).
const STAGES: { id: StageId; name: string; href: string | null; page?: string }[] = [
  { id: "I", name: "Evaluate", href: "/intake/", page: "Intake · Benchmark" },
  { id: "II·a", name: "Endeavor", href: null },
  { id: "II·b", name: "Evidence", href: "/citations/", page: "Citation review" },
  { id: "III", name: "Draft", href: null },
  { id: "IV", name: "Forms", href: "/forms/", page: "Forms wizard" },
  { id: "V", name: "Package", href: null },
  { id: "R", name: "RFE", href: null },
];

let stateCache: string | null = null;

function parseStages(stateMd: string, visible: typeof STAGES): Record<StageId, StageStatus> {
  const out = {} as Record<StageId, StageStatus>;
  visible.forEach((s) => { out[s.id] = "todo"; });
  let sawCurrent = false;
  for (const line of stateMd.split("\n")) {
    const m = line.match(/^\s*-\s*\[( |x|X)\]\s+(I{1,3}V?|IV|V|R)(·[ab])?\s/);
    if (!m) continue;
    const id = (m[2] + (m[3] || "")) as StageId;
    if (!(id in out)) continue;
    if (m[1].toLowerCase() === "x") out[id] = "done";
    else if (!sawCurrent && (line.includes("←") || line.includes("<-"))) {
      out[id] = "current";
      sawCurrent = true;
    }
  }
  if (!sawCurrent) {
    const firstTodo = visible.find((s) => out[s.id] === "todo");
    if (firstTodo) out[firstTodo.id] = "current";
  }
  return out;
}

export function Header({ active, progress }: {
  active: "overview" | "intake" | "benchmark" | "citations" | "forms";
  progress?: { label: string; done: number; total: number };
}) {
  const [stateMd, setStateMd] = useState<string>(stateCache || "");
  useEffect(() => {
    if (stateCache != null) return;
    api("/api/state").then((r) => {
      const md: string = r.state_md || "";
      stateCache = md;
      setStateMd(md);
    }).catch(() => { stateCache = ""; });
  }, []);

  const hasRfe = /^\s*-\s*\[( |x|X)\]\s+R\s/m.test(stateMd);
  const visibleStages = hasRfe ? STAGES : STAGES.filter((s) => s.id !== "R");
  const stages = parseStages(stateMd, visibleStages);
  const activeStage: StageId | null =
    active === "intake" || active === "benchmark" ? "I"
      : active === "citations" ? "II·b"
      : active === "forms" ? "IV" : null;

  return (
    <header className="mb-6">
      <div className="flex items-baseline justify-between flex-wrap gap-2 mb-4">
        <a href={withToken("/")} className="hover:opacity-80">
          <span className="docket-line text-[--docket]">OpenNIW</span>
          <span className="text-xs text-[#4f5a55] ml-2">
            runs only on your computer · your case folder is the only storage
          </span>
        </a>
        {active !== "overview" && (
          <a href={withToken("/")} className="docket-line text-[#4f5a55] hover:text-[--ink] hover:underline">
            case overview
          </a>
        )}
      </div>

      {/* global journey stepper */}
      <div className="border border-[--rule] bg-white px-4 py-3 overflow-x-auto">
        <div className="flex items-start" style={{ minWidth: hasRfe ? 640 : 560 }}>
          {visibleStages.map((s, i) => {
            const st = stages[s.id];
            const isHere = s.id === activeStage;
            const clickable = !!s.href;
            const node = (
              <div className="flex flex-col items-center gap-1 min-w-0">
                <div className={`w-6 h-6 grid place-items-center border text-[0.7rem] font-mono
                    ${st === "done" ? "bg-[--docket] border-[--docket] text-white"
                      : st === "current" ? "bg-white border-[--docket] text-[--docket] font-bold"
                      : "bg-[--field] border-[--rule] text-[#9aa39e]"}`}
                     style={{ borderRadius: 2 }}>
                  {st === "done" ? "✓" : s.id.replace("·", "")}
                </div>
                <div className={`docket-line !text-[0.7rem] text-center leading-tight
                    ${isHere ? "text-[--docket] font-semibold underline underline-offset-4"
                      : st === "done" ? "text-[--ink]"
                      : st === "current" ? "text-[--ink]" : "text-[#9aa39e]"}`}>
                  {s.id} {s.name}
                </div>
                <span className="border px-1 py-px text-[0.6rem] leading-none"
                      style={clickable
                        ? { color: "#1f6f54", borderColor: "#1f6f54", background: "#fff" }
                        : { color: "#8a8f8a", borderColor: "#d8d5cc" }}>
                  {clickable ? "browser" : "agent chat"}
                </span>
              </div>
            );
            return (
              <div key={s.id} className="flex items-start flex-1 last:flex-none">
                {clickable ? (
                  <a href={withToken(s.href!)} className="hover:opacity-75">{node}</a>
                ) : (
                  <div title="This stage happens in the chat with your agent.">{node}</div>
                )}
                {i < visibleStages.length - 1 && (
                  <div className="flex-1 h-[2px] mt-3 mx-1"
                       style={{ background: st === "done" ? "#1f6f54" : "#d8d5cc" }} />
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* local progress within the current page */}
      {progress && (
        <div className="mt-2">
          <div className="flex justify-between items-baseline">
            <span className="docket-line text-[#4f5a55]">
              {activeStage ? `Stage ${activeStage} progress` : "Progress"}
            </span>
            <span className="docket-line text-[--docket]">{progress.label}</span>
          </div>
          <div className="h-[4px] bg-[--field] border border-[--rule] mt-1">
            <div className="h-full bg-[--docket] transition-all"
                 style={{ width: `${Math.min(100, 100 * progress.done / Math.max(1, progress.total))}%` }} />
          </div>
        </div>
      )}
    </header>
  );
}

// What each browser step is called, what the agent does right after it,
// and what comes later — drives the finish overlay's handoff flow.
const STEP_FLOW: Record<string, { name: string; agentNext: string; later: string }> = {
  intake: {
    name: "Intake",
    agentNext: "fetch and read everything you provided, download your papers, and build your profile",
    later: "it opens the benchmark comparison page for you",
  },
  benchmark: {
    name: "Peer benchmark",
    agentNext: "fold your percentiles into an honest, prong-by-prong written evaluation",
    later: "Stage II·a — defining your endeavor, in chat",
  },
  citations: {
    name: "Citation review",
    agentNext: "turn your picks into the Citation Examples document with highlighted PDFs",
    later: "drafting continues in chat",
  },
  forms: {
    name: "Forms wizard",
    agentNext: "review your answers, list any hand-fill fields, and walk you through printing and signing",
    later: "Stage V — assembling the filing package",
  },
};

export function FinishBar({ summary, beforeFinish, stepId }: {
  summary: () => Record<string, any>;
  beforeFinish?: () => Promise<void>;
  stepId?: "intake" | "benchmark" | "citations" | "forms";
}) {
  const [state, setState] = useState<"open" | "busy" | "done" | "later">("open");
  const flow = STEP_FLOW[stepId || ""] || {
    name: "This step", agentNext: "pick up from your case folder", later: "the next stage",
  };

  async function finish(kind: "done" | "later") {
    setState("busy");
    try {
      if (beforeFinish) await beforeFinish();
      await api(`/api/${kind === "done" ? "done" : "later"}`, {
        method: "POST", body: { summary: summary() },
      });
      setState(kind === "done" ? "done" : "later");
    } catch {
      setState("open");
    }
  }

  if (state === "done" || state === "later") {
    const done = state === "done";
    return (
      <div className="fixed inset-0 bg-[--paper] z-50 grid place-items-center overflow-y-auto">
        <div className="max-w-lg px-6 py-10 w-full">
          <div className="docket-line text-[--docket] mb-2 text-center">
            {done ? `${flow.name} — complete ✓` : `${flow.name} — saved for later`}
          </div>
          <h2 className="text-3xl text-center mb-8"
              style={{ fontFamily: "var(--font-serif), serif" }}>
            {done ? "Now return to your agent" : "Come back anytime"}
          </h2>

          {/* handoff flow: where you were → where to go now → what's later */}
          <div className="grid gap-2 mb-8">
            <div className="border border-[--rule] bg-white px-4 py-3 flex items-center gap-3 opacity-70">
              <span className="docket-line border px-1.5 py-0.5 shrink-0"
                    style={{ color: "#1f6f54", borderColor: "#1f6f54" }}>browser</span>
              <span className="text-sm">
                {flow.name} — {done ? "done ✓" : "progress saved"}
              </span>
            </div>
            <div className="text-center docket-line text-[#4f5a55]">↓</div>
            <div className="border-2 border-[--docket] bg-white px-4 py-3 flex items-center gap-3">
              <span className="docket-line border px-1.5 py-0.5 shrink-0 verify-nag"
                    style={{ color: "#fff", background: "#1f6f54", borderColor: "#1f6f54" }}>
                now: agent chat
              </span>
              <span className="text-sm">
                Switch back to your terminal (Claude Code / Codex)
                {done ? <> — your agent will {flow.agentNext}.</> : " whenever you're ready."}
              </span>
            </div>
            {done && (
              <>
                <div className="text-center docket-line text-[#4f5a55]">↓</div>
                <div className="border border-[--rule] bg-[--field] px-4 py-3 flex items-center gap-3 opacity-70">
                  <span className="docket-line border border-[--rule] px-1.5 py-0.5 shrink-0 text-[#4f5a55]">later</span>
                  <span className="text-sm text-[#4f5a55]">{flow.later}</span>
                </div>
              </>
            )}
          </div>

          <p className="text-xs text-center text-[#4f5a55]">
            Everything is saved in your case folder. You can close this tab.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex gap-2 justify-end border-t border-[--rule] pt-4 mt-8">
      <button className="btn-quiet" disabled={state === "busy"}
              onClick={() => finish("later")}>
        Save and finish later
      </button>
      <button className="btn" disabled={state === "busy"}
              onClick={() => finish("done")}>
        {state === "busy" ? "…" : "Done — return to the agent"}
      </button>
    </div>
  );
}
