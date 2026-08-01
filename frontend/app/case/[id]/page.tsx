"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Md from "@/components/Md";
import { api, waitForJob } from "@/lib/api";

export default function CaseOverview() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<any>(null);
  const [showReport, setShowReport] = useState(false);
  const [ingestBusy, setIngestBusy] = useState(false);
  const [scholar, setScholar] = useState("");
  const [homepage, setHomepage] = useState("");
  const [cv, setCv] = useState<File | null>(null);

  const load = () => api(`/api/cases/${id}`).then(setData).catch(() => {});
  useEffect(() => {
    load();
  }, [id]);

  async function ingest() {
    setIngestBusy(true);
    try {
      const form = new FormData();
      form.append("scholar_url", scholar);
      form.append("homepage_url", homepage);
      if (cv) form.append("cv", cv);
      const res = await api(`/api/cases/${id}/ingest`, { method: "POST", form });
      await waitForJob(res.job_id);
      await load();
    } finally {
      setIngestBusy(false);
    }
  }

  if (!data) return <p className="docket-line">Loading case…</p>;
  const p = data.profile?.parsed || {};
  const c = data.counts || {};

  return (
    <div className="grid lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 grid gap-6 content-start">
        <section className="border border-[--rule] bg-white">
          <div className="rule-b px-5 py-3 docket-line">Case record</div>
          <div className="px-5 py-4 grid sm:grid-cols-2 gap-x-6 gap-y-3 text-sm">
            <div><span className="docket-line text-[#6b7570]">Title</span><br />{data.title}</div>
            <div><span className="docket-line text-[#6b7570]">Field</span><br />{data.field || p.field || "—"}</div>
            <div><span className="docket-line text-[#6b7570]">Applicant</span><br />{p.name || "—"}</div>
            <div><span className="docket-line text-[#6b7570]">Citations / h-index</span><br />
              {p.metrics?.citations ?? "—"} / {p.metrics?.h_index ?? "—"}</div>
            <div><span className="docket-line text-[#6b7570]">Publications on record</span><br />
              {p.publications?.length ?? 0}</div>
            <div><span className="docket-line text-[#6b7570]">Evidence provided</span><br />
              {c.evidence_provided ?? 0} of {c.evidence_total ?? 0}</div>
          </div>
        </section>

        {data.evaluation && (
          <section className="border border-[--rule] bg-white">
            <div className="rule-b px-5 py-3 flex justify-between items-center">
              <span className="docket-line">Evaluation — tier: {data.evaluation.tier || "—"}</span>
              <button className="docket-line text-[--docket] hover:underline"
                      onClick={() => setShowReport(!showReport)}>
                {showReport ? "Collapse" : "Read full report"}
              </button>
            </div>
            {showReport && (
              <div className="px-5 py-4">
                <Md>{data.evaluation.report_md || ""}</Md>
              </div>
            )}
          </section>
        )}
      </div>

      <aside className="grid gap-6 content-start">
        <section className="border border-[--docket] bg-[--field] px-5 py-4">
          <div className="docket-line text-[--docket] mb-2">Feed the record</div>
          <p className="text-sm mb-3">
            Add or refresh sources — the profile, checklist and drafts all
            draw from here.
          </p>
          <div className="grid gap-2">
            <input placeholder="Google Scholar URL" value={scholar} onChange={(e) => setScholar(e.target.value)} />
            <input placeholder="Homepage URL" value={homepage} onChange={(e) => setHomepage(e.target.value)} />
            <input type="file" accept=".pdf" className="!p-1.5" onChange={(e) => setCv(e.target.files?.[0] || null)} />
            <button className="btn" onClick={ingest} disabled={ingestBusy}>
              {ingestBusy ? <span className="drafting-caret">Analyzing</span> : "Analyze sources"}
            </button>
          </div>
        </section>
        <section className="border border-[--rule] bg-white px-5 py-4 text-sm">
          <div className="docket-line mb-2">Docket status</div>
          <ul className="grid gap-1.5 docket-line text-[#3c4642]">
            <li>Evidence — {c.evidence_provided ?? 0}/{c.evidence_total ?? 0} provided</li>
            <li>Recommenders — {c.recommenders ?? 0} listed</li>
            <li>Documents — {c.documents ?? 0} drafted</li>
            <li>Forms — {c.filled_forms ?? 0} filled</li>
          </ul>
        </section>
      </aside>
    </div>
  );
}
