"use client";
import { useState } from "react";
import { api, withToken } from "@/lib/api";

export function Header({ active }: { active: "overview" | "forms" | "citations" }) {
  const tabs: [string, string, string][] = [
    ["overview", "Overview", "/"],
    ["forms", "IV · Forms", "/forms/"],
    ["citations", "II·b · Citations", "/citations/"],
  ];
  return (
    <header className="border-b border-[--rule] mb-6 pb-3 flex items-end justify-between flex-wrap gap-3">
      <div>
        <div className="docket-line text-[--docket]">OpenNIW — local companion</div>
        <div className="text-xs text-[#4f5a55]">
          Runs only on your computer · reads and writes only your case folder
        </div>
      </div>
      <nav className="flex gap-1">
        {tabs.map(([key, label, href]) => (
          <a key={key} href={withToken(href)}
             className={`docket-line px-3 py-1.5 border ${key === active ? "border-[--docket] text-[--docket]" : "border-[--rule] hover:border-[--ink]"}`}>
            {label}
          </a>
        ))}
      </nav>
    </header>
  );
}

export function FinishBar({ summary, beforeFinish }: {
  summary: () => Record<string, any>;
  beforeFinish?: () => Promise<void>;
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
              ? "Everything is saved to your case folder. Close this tab and continue in your chat."
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
