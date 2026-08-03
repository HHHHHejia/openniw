"use client";
import { useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";
import { Header, FinishBar } from "@/components/session";

type Card = {
  key: string;
  cited_title?: string;
  citing_title?: string;
  venue?: string;
  year?: number;
  authors?: string[];
  institutions?: { name?: string; country?: string }[];
  score?: number;
  use_type?: string;
  quote?: string;
  note?: string;
};

export default function CitationsPage() {
  const [scored, setScored] = useState<Card[]>([]);
  const [selection, setSelection] = useState<Record<string, any>>({});
  // Opaque server-issued version string (mtime_ns exceeds JS safe integers)
  const [version, setVersion] = useState<string>("0");
  const [saved, setSaved] = useState(false);
  const [conflict, setConflict] = useState(false);
  const [filter, setFilter] = useState<"all" | "selected">("all");

  const load = async () => {
    const r = await api("/api/citations/review");
    setScored(r.scored || []);
    setSelection(r.selection || {});
    setVersion(String(r.version ?? "0"));
    setConflict(false);
  };
  useEffect(() => { load().catch(() => {}); }, []);

  const picked = useMemo(
    () => Object.values(selection).filter((v: any) => v?.selected).length,
    [selection]);

  const perCited = useMemo(() => {
    const count: Record<string, number> = {};
    for (const c of scored) {
      if (selection[c.key]?.selected) {
        const t = c.cited_title || "?";
        count[t] = (count[t] || 0) + 1;
      }
    }
    return count;
  }, [scored, selection]);

  function toggle(key: string) {
    setSelection((s) => ({
      ...s,
      [key]: { ...(s[key] || {}), selected: !s[key]?.selected },
    }));
  }

  function note(key: string, text: string) {
    setSelection((s) => ({ ...s, [key]: { ...(s[key] || {}), note: text } }));
  }

  async function save(): Promise<boolean> {
    try {
      const res = await api("/api/citations/selection", {
        method: "PUT", body: { selection, base_version: version },
      });
      setVersion(res.version);
      setSaved(true);
      setTimeout(() => setSaved(false), 1500);
      return true;
    } catch (e: any) {
      if (e.status === 409) setConflict(true);
      return false;
    }
  }

  const shown = scored.filter(
    (c) => filter === "all" || selection[c.key]?.selected);

  return (
    <div className="max-w-4xl mx-auto px-6 py-6">
      <Header active="citations"
              progress={{ label: `${picked} of ~10 examples selected`,
                          done: Math.min(picked, 10), total: 10 }} />
      <div className="flex items-center justify-between flex-wrap gap-3 mb-2">
        <h1 className="text-2xl" style={{ fontFamily: "var(--font-serif), serif" }}>
          Citation portfolio — pick your best ~10
        </h1>
        <div className="flex items-center gap-3">
          <span className="docket-line text-[--docket]">{picked} selected</span>
          <button className="btn" onClick={save}>{saved ? "Saved ✓" : "Save selection"}</button>
        </div>
      </div>
      <p className="text-sm text-[#4f5a55] mb-1">
        Your agent scored each citing paper by depth of use (HOW your work was
        used beats WHO cited it). Aim for coverage across several of your
        papers — max 2 examples per cited work is the usual portfolio shape.
      </p>
      {Object.keys(perCited).length > 0 && (
        <p className="docket-line text-[#4f5a55] mb-4">
          {Object.entries(perCited).map(([t, n]) =>
            `${n}× ${t.slice(0, 40)}${t.length > 40 ? "…" : ""}`).join(" · ")}
        </p>
      )}
      {conflict && (
        <div className="border border-[--stamp] text-[--stamp] px-4 py-2 mb-4 flex items-center justify-between">
          <span className="docket-line">Selection changed on disk.</span>
          <button className="docket-line underline" onClick={() => load()}>
            Reload latest
          </button>
        </div>
      )}
      <div className="flex gap-1 mb-4">
        {(["all", "selected"] as const).map((f) => (
          <button key={f}
                  className={`docket-line px-3 py-1.5 border ${filter === f ? "border-[--docket] text-[--docket]" : "border-[--rule]"}`}
                  onClick={() => setFilter(f)}>
            {f === "all" ? `All (${scored.length})` : `Selected (${picked})`}
          </button>
        ))}
      </div>

      {scored.length === 0 && (
        <div className="border border-[--rule] bg-white px-5 py-8 text-center">
          <p className="docket-line text-[#4f5a55]">
            No scored citations yet — your agent writes citations/scored.json
            after the harvest &amp; scoring pass. Ask it to run the citation
            pipeline first.
          </p>
        </div>
      )}

      <div className="grid gap-3">
        {shown.map((c) => {
          const sel = selection[c.key]?.selected;
          return (
            <div key={c.key}
                 className={`border bg-white px-5 py-4 ${sel ? "border-[--docket]" : "border-[--rule]"}`}>
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <div className="text-sm font-medium leading-snug">{c.citing_title}</div>
                  <div className="docket-line text-[#4f5a55] mt-0.5">
                    {[c.venue, c.year, (c.authors || []).slice(0, 3).join(", ")
                      + ((c.authors || []).length > 3 ? " et al." : "")]
                      .filter(Boolean).join(" · ")}
                  </div>
                  <div className="docket-line mt-1">
                    {c.use_type && (
                      <span className="border border-[--docket] text-[--docket] px-1 mr-2">
                        {c.use_type}
                      </span>
                    )}
                    {typeof c.score === "number" && <span>depth {c.score}/9</span>}
                    {c.cited_title && (
                      <span className="text-[#4f5a55]"> · cites: {c.cited_title.slice(0, 50)}{c.cited_title.length > 50 ? "…" : ""}</span>
                    )}
                  </div>
                </div>
                <button type="button"
                        className={`docket-line shrink-0 px-3 py-1.5 border ${sel ? "border-[--docket] bg-[--docket] text-white" : "border-[--rule] hover:border-[--docket]"}`}
                        onClick={() => toggle(c.key)}>
                  {sel ? "Selected ✓" : "Select"}
                </button>
              </div>
              {c.quote && (
                <blockquote className="mt-2 text-sm border-l-2 border-[--rule] pl-3 text-[#333] italic">
                  “{c.quote}”
                </blockquote>
              )}
              {sel && (
                <input className="mt-2 !text-xs" placeholder="Optional note for your agent (why this one, anything to verify…)"
                       value={selection[c.key]?.note || ""}
                       onChange={(e) => note(c.key, e.target.value)} />
              )}
            </div>
          );
        })}
      </div>

      <FinishBar
        stepId="citations"
        beforeFinish={async () => { await save(); }}
        summary={() => ({ citations_selected: picked })}
      />
    </div>
  );
}
