"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Md from "@/components/Md";
import { api, downloadWithAuth, waitForJob } from "@/lib/api";

const DOC_ORDER = [
  ["pes", "Proposed Endeavor Statement", "The frozen endeavor sentence + your future research plan. Draft this first."],
  ["reco_letter", "Support letters", "One per recommender, each with a distinct angle. Add recommenders below first."],
  ["petition_letter", "Petition Letter", "The full legal brief arguing the three Dhanasar prongs, cited to your exhibits."],
  ["exhibit_list", "Index of Exhibits", "Built from evidence marked provided."],
  ["cover_letter", "Filing cover letter", "One page, lockbox order."],
] as const;

export default function DocumentsPage() {
  const { id } = useParams<{ id: string }>();
  const [docs, setDocs] = useState<any[]>([]);
  const [recs, setRecs] = useState<any[]>([]);
  const [busyKind, setBusyKind] = useState<string | null>(null);
  const [editing, setEditing] = useState<any | null>(null);
  const [editText, setEditText] = useState("");
  const [error, setError] = useState("");
  const [newRec, setNewRec] = useState({ name: "", title: "", org: "", relationship: "dependent", angle: "" });

  const load = async () => {
    setDocs(await api(`/api/cases/${id}/documents`));
    setRecs(await api(`/api/cases/${id}/recommenders`));
  };
  useEffect(() => {
    load().catch(() => {});
  }, [id]);

  async function generate(doc_type: string, recommender_id?: string) {
    setError("");
    setBusyKind(doc_type + (recommender_id || ""));
    try {
      const res = await api(`/api/cases/${id}/documents/generate`, {
        method: "POST",
        body: { doc_type, recommender_id } as any,
      });
      await waitForJob(res.job_id);
      await load();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setBusyKind(null);
    }
  }

  async function saveEdit() {
    await api(`/api/cases/${id}/documents/${editing.id}`, {
      method: "PUT",
      body: { content_md: editText } as any,
    });
    setEditing(null);
    load();
  }

  async function addRec() {
    if (!newRec.name) return;
    await api(`/api/cases/${id}/recommenders`, { method: "POST", body: newRec as any });
    setNewRec({ name: "", title: "", org: "", relationship: "dependent", angle: "" });
    load();
  }

  const docFor = (t: string, recId?: string) =>
    docs.find((d) => d.doc_type === t && (t !== "reco_letter" || d.recommender_id === recId));

  if (editing) {
    return (
      <div>
        <div className="flex justify-between items-center mb-4 flex-wrap gap-2">
          <h1 className="text-2xl" style={{ fontFamily: "var(--font-serif), serif" }}>
            Editing — {editing.doc_type} v{editing.version}
          </h1>
          <div className="flex gap-2">
            <button className="btn-quiet" onClick={() => setEditing(null)}>Discard</button>
            <button className="btn" onClick={saveEdit}>Save changes</button>
          </div>
        </div>
        <div className="grid lg:grid-cols-2 gap-4">
          <textarea rows={30} value={editText} onChange={(e) => setEditText(e.target.value)}
                    className="font-mono !text-xs leading-relaxed" />
          <div className="border border-[--rule] bg-white px-5 py-4 max-h-[75vh] overflow-y-auto">
            <Md>{editText}</Md>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl mb-2" style={{ fontFamily: "var(--font-serif), serif" }}>
        Drafting desk
      </h1>
      <p className="text-sm text-[#3c4642] max-w-2xl mb-6">
        Drafts follow the structure of real approved filings. Facts come only
        from your record — anything missing is flagged <span className="docket-line">[TODO]</span> instead
        of invented. Review every word before signing; you are the petitioner.
      </p>
      {error && <p className="text-sm text-[--stamp] mb-4">{error}</p>}

      <div className="grid gap-6">
        {DOC_ORDER.map(([type, title, hint]) => (
          <section key={type} className="border border-[--rule] bg-white">
            <div className="rule-b px-5 py-3 flex items-center justify-between flex-wrap gap-2">
              <div>
                <span className="docket-line text-[--docket] mr-3">{type}</span>
                <span className="font-medium text-sm">{title}</span>
              </div>
              {type !== "reco_letter" && (
                <div className="flex gap-2 items-center">
                  {docFor(type) && (
                    <>
                      <button className="docket-line hover:text-[--docket]" onClick={() => {
                        const d = docFor(type);
                        setEditing(d);
                        setEditText(d.content_md);
                      }}>Edit</button>
                      <button className="docket-line hover:text-[--docket]"
                              onClick={() => downloadWithAuth(`/api/cases/${id}/documents/${docFor(type).id}/docx`, `${type}.docx`)}>
                        DOCX
                      </button>
                    </>
                  )}
                  <button className="btn-quiet !py-1.5" disabled={busyKind !== null}
                          onClick={() => generate(type)}>
                    {busyKind === type ? (
                      <span className="drafting-caret">Drafting</span>
                    ) : docFor(type) ? `Redraft (v${docFor(type).version + 1})` : "Draft"}
                  </button>
                </div>
              )}
            </div>
            <div className="px-5 py-3 text-sm text-[#3c4642]">
              {hint}
              {type === "reco_letter" && (
                <div className="mt-3 grid gap-3">
                  {recs.map((r) => {
                    const d = docFor("reco_letter", r.id);
                    return (
                      <div key={r.id} className="flex items-center justify-between flex-wrap gap-2 border border-[--rule] px-4 py-2.5">
                        <div>
                          <span className="font-medium">{r.name}</span>{" "}
                          <span className="docket-line text-[#6b7570]">{r.relationship} · {r.org || "org?"} · {r.angle || "no angle set"}</span>
                        </div>
                        <div className="flex gap-2 items-center">
                          {d && (
                            <>
                              <button className="docket-line hover:text-[--docket]" onClick={() => { setEditing(d); setEditText(d.content_md); }}>Edit</button>
                              <button className="docket-line hover:text-[--docket]"
                                      onClick={() => downloadWithAuth(`/api/cases/${id}/documents/${d.id}/docx`, `letter_${r.name}.docx`)}>DOCX</button>
                            </>
                          )}
                          <button className="btn-quiet !py-1" disabled={busyKind !== null}
                                  onClick={() => generate("reco_letter", r.id)}>
                            {busyKind === "reco_letter" + r.id ? <span className="drafting-caret">Drafting</span> : d ? "Redraft" : "Draft"}
                          </button>
                        </div>
                      </div>
                    );
                  })}
                  <div className="grid sm:grid-cols-5 gap-2 items-end border-t border-[--rule] pt-3">
                    <input placeholder="Name" value={newRec.name} onChange={(e) => setNewRec({ ...newRec, name: e.target.value })} />
                    <input placeholder="Title & org" value={newRec.org} onChange={(e) => setNewRec({ ...newRec, org: e.target.value })} />
                    <select value={newRec.relationship} onChange={(e) => setNewRec({ ...newRec, relationship: e.target.value })}>
                      <option value="dependent">dependent (knows you)</option>
                      <option value="independent">independent (cited you)</option>
                    </select>
                    <input placeholder="Angle (e.g. national importance)" value={newRec.angle} onChange={(e) => setNewRec({ ...newRec, angle: e.target.value })} />
                    <button className="btn-quiet !py-2" onClick={addRec}>Add</button>
                  </div>
                  <p className="docket-line text-[#6b7570]">
                    Max 4 letters. Dependent letters carry more weight now; independents should have cited your work.
                  </p>
                </div>
              )}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}
