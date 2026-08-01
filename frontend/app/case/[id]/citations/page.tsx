"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api, waitForJob } from "@/lib/api";

const USE_COLOR: Record<string, string> = {
  implemented: "var(--docket)",
  compared_favorably: "var(--docket)",
  utilized: "var(--docket)",
  verified: "var(--docket)",
  extensive: "#4a6b2a",
  moderate: "#8a7a2a",
  background: "#4f5a55",
  passing: "#a8a89e",
};

export default function CitationsPage() {
  const { id } = useParams<{ id: string }>();
  const [summary, setSummary] = useState<any>(null);
  const [rows, setRows] = useState<any[]>([]);
  const [filter, setFilter] = useState<string>("scored");
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [candidates, setCandidates] = useState<any[] | null>(null);
  const [open, setOpen] = useState<string | null>(null);

  const load = async (f = filter) => {
    setSummary(await api(`/api/cases/${id}/citations/summary`));
    setRows(await api(`/api/cases/${id}/citations${f ? `?status=${f}` : ""}`));
  };
  useEffect(() => {
    load().catch(() => {});
  }, [id]);

  async function run(step: "harvest" | "verify" | "deliverables") {
    setBusy(step);
    setError("");
    try {
      const res = await api(`/api/cases/${id}/citations/${step}`, { method: "POST" });
      await waitForJob(res.job_id, { timeoutMs: 30 * 60 * 1000 });
      await load();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setBusy(null);
    }
  }

  async function setStatus(cid: string, status: string) {
    await api(`/api/cases/${id}/citations/${cid}/status`, {
      method: "PUT",
      body: { status } as any,
    });
    load();
  }

  async function loadCandidates() {
    setCandidates(await api(`/api/cases/${id}/citations/recommender-candidates`));
  }

  async function addRecommender(c: any) {
    await api(`/api/cases/${id}/recommenders`, {
      method: "POST",
      body: {
        name: c.name,
        org: c.institutions?.[0] || "",
        relationship: "independent",
        angle: `Cited the work in: ${c.citing_papers.slice(0, 2).join("; ")}`,
      } as any,
    });
    setCandidates((cs) => (cs || []).filter((x) => x.name !== c.name));
  }

  const s = summary || {};

  return (
    <div>
      <h1 className="text-2xl mb-2" style={{ fontFamily: "var(--font-serif), serif" }}>
        Citation pipeline
      </h1>
      <p className="text-sm text-[#3c4642] max-w-2xl mb-6">
        The most labor-intensive part of a NIW case, automated: every citing
        paper is harvested, screened for independence, verified in full text,
        and scored by <em>how</em> it uses your work — not who wrote it.
        Negative citations are quarantined automatically.
      </p>

      {/* Pipeline controls */}
      <div className="flex gap-2 flex-wrap mb-4">
        <button className="btn-quiet" disabled={busy !== null} onClick={() => run("harvest")}>
          {busy === "harvest" ? <span className="drafting-caret">Harvesting from OpenAlex</span> : "1 · Harvest citing papers"}
        </button>
        <button className="btn-quiet" disabled={busy !== null || !s.usable_pool} onClick={() => run("verify")}>
          {busy === "verify" ? <span className="drafting-caret">Verifying & scoring</span> : "2 · Verify + score"}
        </button>
        <button className="btn" disabled={busy !== null || !s.selected} onClick={() => run("deliverables")}>
          {busy === "deliverables" ? <span className="drafting-caret">Building</span> : "3 · Build highlighted PDFs + summary doc"}
        </button>
        <button className="btn-quiet" disabled={!s.selected} onClick={loadCandidates}>
          Recommender candidates
        </button>
      </div>
      {error && <p className="text-sm text-[--stamp] mb-4">{error}</p>}

      {/* Docket summary */}
      {s.total > 0 && (
        <div className="border border-[--rule] bg-white px-5 py-3 mb-6 flex flex-wrap gap-x-6 gap-y-1 docket-line">
          <span>{s.total} citing papers</span>
          <span className="text-[--docket]">{s.independent} independent ({s.independent_pct}%)</span>
          <span>{s.usable_pool} usable pool</span>
          <span>{s.verified} verified in text</span>
          {s.false_positives > 0 && <span className="text-[--stamp]">{s.false_positives} index false-positives</span>}
          {s.negative > 0 && <span className="text-[--stamp]">{s.negative} negative (quarantined)</span>}
          {s.needs_review > 0 && <span style={{ color: "#8a7a2a" }}>{s.needs_review} same-surname review</span>}
          <span className="text-[--docket]">{s.selected} selected</span>
        </div>
      )}

      {/* Recommender candidates panel */}
      {candidates && (
        <section className="border border-[--docket] bg-[--field] px-5 py-4 mb-6">
          <div className="docket-line text-[--docket] mb-2">
            Independent recommender candidates (authors of your selected citations)
          </div>
          {candidates.length === 0 && <p className="text-sm">Select citations first.</p>}
          <div className="grid gap-2">
            {candidates.slice(0, 8).map((c) => (
              <div key={c.name} className="flex items-center justify-between gap-2 text-sm bg-white border border-[--rule] px-4 py-2">
                <div>
                  <span className="font-medium">{c.name}</span>{" "}
                  <span className="docket-line text-[#4f5a55]">
                    {c.n_citations_discussable} citation{c.n_citations_discussable > 1 ? "s" : ""} · {c.institutions?.[0] || "institution unknown"}{c.us_based ? " · US" : ""}
                  </span>
                </div>
                <button className="btn-quiet !py-1" onClick={() => addRecommender(c)}>Add</button>
              </div>
            ))}
          </div>
          <p className="docket-line text-[#4f5a55] mt-2">
            Strongest: can discuss ≥2 notable citations; U.S.-based preferred; no students.
          </p>
        </section>
      )}

      {/* Filter + table */}
      <div className="flex gap-1 mb-3 flex-wrap">
        {[["scored", "Scored"], ["selected", "Selected"], ["harvested", "Pool"], ["verified", "Verified/rejected"], ["", "All"]].map(([f, label]) => (
          <button key={f}
                  className={`docket-line px-3 py-1.5 border ${filter === f ? "border-[--docket] text-[--docket]" : "border-[--rule]"}`}
                  onClick={() => { setFilter(f); load(f); }}>
            {label}
          </button>
        ))}
      </div>
      <div className="border border-[--rule] bg-white divide-y divide-[--rule]">
        {rows.length === 0 && (
          <p className="px-5 py-8 text-sm text-[#4f5a55] text-center">
            Nothing here yet — run the pipeline steps above. Harvest needs your
            publications in the profile (Overview → Analyze sources).
          </p>
        )}
        {rows.map((r) => (
          <div key={r.id} className="px-5 py-3">
            <div className="flex items-start justify-between gap-3 flex-wrap">
              <button className="text-left text-sm max-w-[70%] hover:text-[--docket]"
                      onClick={() => setOpen(open === r.id ? null : r.id)}>
                <span className="font-medium">{r.citing_title}</span>
                <span className="block docket-line text-[#4f5a55] mt-0.5">
                  {r.citing_venue || "venue?"} · {r.citing_year || "?"} · cites “{r.cited_title.slice(0, 60)}…”
                </span>
              </button>
              <div className="flex gap-2 items-center docket-line">
                {r.negative && <span className="text-[--stamp] border border-[--stamp] px-1.5">NEGATIVE</span>}
                {r.same_surname_flag && <span style={{ color: "#8a7a2a" }}>review</span>}
                {r.use_type && (
                  <span style={{ color: USE_COLOR[r.use_type] || "inherit" }}>
                    {r.use_type} {r.score ? `· ${r.score}/9` : ""}
                  </span>
                )}
                <span className={r.status === "selected" ? "text-[--docket]" : "text-[#4f5a55]"}>{r.status}</span>
              </div>
            </div>
            {open === r.id && (
              <div className="mt-3 text-sm text-[#3c4642]">
                {r.quote_context && (
                  <blockquote className="border-l-2 border-[--rule] pl-3 mb-2 italic">
                    “{r.quote_context.slice(0, 600)}”
                  </blockquote>
                )}
                {r.reject_reason && <p className="docket-line text-[--stamp] mb-2">{r.reject_reason}</p>}
                <div className="flex gap-2">
                  {r.status !== "selected" && !r.negative && r.verified_in_text && (
                    <button className="docket-line px-2 py-1 border border-[--docket] text-[--docket]"
                            onClick={() => setStatus(r.id, "selected")}>select</button>
                  )}
                  {r.status === "selected" && (
                    <button className="docket-line px-2 py-1 border border-[--rule]"
                            onClick={() => setStatus(r.id, "scored")}>deselect</button>
                  )}
                  <button className="docket-line px-2 py-1 border border-[--rule]"
                          onClick={() => setStatus(r.id, "rejected")}>reject</button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
      <p className="docket-line text-[#4f5a55] mt-3">
        Deliverables land in Documents (Citation Examples) and in the filing package (highlighted PDFs).
      </p>
    </div>
  );
}
