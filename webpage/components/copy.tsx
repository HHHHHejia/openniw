"use client";
import { useState } from "react";

export function CopyBlock({ copyText, className, children }: {
  copyText: string;
  className?: string;
  children: React.ReactNode;
}) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(copyText);
    } catch {
      // clipboard API blocked — fall back to a selectable prompt
      window.prompt("Copy this command:", copyText);
      return;
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 1600);
  }

  return (
    <div className="relative group mb-2">
      <pre className={`px-4 py-3 pr-20 text-sm font-mono overflow-x-auto ${className || "bg-white border border-[--rule]"}`}>
        {children}
      </pre>
      <button
        type="button"
        onClick={copy}
        aria-label="Copy command"
        className={`docket-line absolute top-2 right-2 px-2 py-1 border bg-white
          ${copied ? "border-[--docket] text-[--docket]" : "border-[--rule] text-[#4f5a55] hover:border-[--docket] hover:text-[--docket]"}`}
      >
        {copied ? "copied ✓" : "copy"}
      </button>
    </div>
  );
}
