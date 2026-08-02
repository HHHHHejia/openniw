"use client";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { api } from "@/lib/api";
import { Header } from "@/components/session";

export default function Overview() {
  const [stateMd, setStateMd] = useState<string>("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api("/api/state")
      .then((r) => setStateMd(r.state_md || ""))
      .catch((e) => setError(String(e.message || e)));
  }, []);

  return (
    <div className="max-w-3xl mx-auto px-6 py-6">
      <Header active="overview" />
      <h1 className="text-2xl mb-1" style={{ fontFamily: "var(--font-serif), serif" }}>
        Case overview
      </h1>
      <p className="text-sm text-[#4f5a55] mb-6">
        This is your case&apos;s STATE.md — the working state your agent reads at
        the start of every session and updates after every step. Edit it in
        chat, not here.
      </p>
      {error && (
        <p className="docket-line text-[--stamp]">
          Could not load state: {error}. Open this page from the URL your
          agent printed (it carries the session token).
        </p>
      )}
      {stateMd ? (
        <article className="prose-doc border border-[--rule] bg-white px-6 py-5">
          <ReactMarkdown>{stateMd}</ReactMarkdown>
        </article>
      ) : !error ? (
        <p className="docket-line text-[#4f5a55]">
          No STATE.md yet — your agent creates it when the case starts.
        </p>
      ) : null}
      <p className="docket-line text-[#4f5a55] mt-6">
        OpenNIW is document preparation, not legal advice.
      </p>
    </div>
  );
}
