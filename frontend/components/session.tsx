"use client";
import { useEffect, useState } from "react";
import { api, withToken } from "@/lib/api";

// The global journey stepper. Stage statuses are parsed live from the
// case's STATE.md (the agent maintains it); stages with a browser page
// link to it, chat-only stages say so.

type StageId = "I" | "II·a" | "II·b" | "III" | "IV" | "V";
type StageStatus = "done" | "current" | "todo";

const STAGES: { id: StageId; name: string; href: string | null; page?: string }[] = [
  { id: "I", name: "Evaluate", href: "/intake/", page: "Intake · Benchmark" },
  { id: "II·a", name: "Endeavor", href: null },
  { id: "II·b", name: "Evidence", href: "/citations/", page: "Citation review" },
  { id: "III", name: "Draft", href: null },
  { id: "IV", name: "Forms", href: "/forms/", page: "Forms wizard" },
  { id: "V", name: "Package", href: null },
];

let stateCache: string | null = null;

function parseStages(stateMd: string): Record<StageId, StageStatus> {
  const out = {} as Record<StageId, StageStatus>;
  STAGES.forEach((s) => { out[s.id] = "todo"; });
  let sawCurrent = false;
  for (const line of stateMd.split("\n")) {
    const m = line.match(/^\s*-\s*\[( |x|X)\]\s+(I{1,3}V?|IV|V)(·[ab])?\s/);
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
    const firstTodo = STAGES.find((s) => out[s.id] === "todo");
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

  const stages = parseStages(stateMd);
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
        <div className="flex items-start min-w-[560px]">
          {STAGES.map((s, i) => {
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
                <div className="text-[0.65rem] leading-none"
                     style={{ color: clickable ? "#1f6f54" : "#9aa39e" }}>
                  {clickable ? (s.page || "open") : "in chat"}
                </div>
              </div>
            );
            return (
              <div key={s.id} className="flex items-start flex-1 last:flex-none">
                {clickable ? (
                  <a href={withToken(s.href!)} className="hover:opacity-75">{node}</a>
                ) : (
                  <div title="This stage happens in the chat with your agent.">{node}</div>
                )}
                {i < STAGES.length - 1 && (
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

export function FinishBar({ summary, beforeFinish, doneMessage }: {
  summary: () => Record<string, any>;
  beforeFinish?: () => Promise<void>;
  doneMessage?: string;
}) {
  const [state, setState] = useState<"open" | "busy" | "done" | "later">("open");

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
    return (
      <div className="fixed inset-0 bg-[--paper] z-50 grid place-items-center">
        <div className="text-center max-w-md px-6">
          <div className="docket-line text-[--docket] mb-3">
            {state === "done" ? "Session finished" : "Saved for later"}
          </div>
          <p className="text-lg" style={{ fontFamily: "var(--font-serif), serif" }}>
            {state === "done"
              ? (doneMessage ||
                 "Everything is saved to your case folder. Close this tab and continue in your chat.")
              : "Your progress is saved. Close this tab — you can reopen the session from your chat anytime."}
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
