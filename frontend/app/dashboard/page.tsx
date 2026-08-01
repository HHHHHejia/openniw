"use client";
import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { api } from "@/lib/api";

function DashboardInner() {
  const router = useRouter();
  const search = useSearchParams();
  const evalId = search.get("eval");
  const [cases, setCases] = useState<any[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [busy, setBusy] = useState(false);
  const [title, setTitle] = useState("My NIW Case");
  const [field, setField] = useState("");

  useEffect(() => {
    api("/api/cases").then((c) => {
      setCases(c);
      setLoaded(true);
    }).catch(() => {});
  }, []);

  async function createCase() {
    setBusy(true);
    try {
      const res = await api("/api/cases", {
        method: "POST",
        body: { title, field, evaluation_id: evalId } as any,
      });
      router.push(`/case/${res.id}`);
    } catch {
      setBusy(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto px-6 py-12">
      <div className="flex justify-between items-center">
        <a href="/" className="docket-line text-[--docket]">← OpenNIW</a>
        <a href="/login" className="docket-line hover:text-[--docket]"
           onClick={() => localStorage.removeItem("openniw_token")}>Sign out</a>
      </div>
      <h1 className="text-3xl mt-8 mb-6" style={{ fontFamily: "var(--font-serif), serif" }}>
        Case files
      </h1>

      {evalId && (
        <div className="border border-[--docket] bg-[--field] px-6 py-5 mb-8">
          <div className="docket-line text-[--docket] mb-2">From your free evaluation</div>
          <div className="grid sm:grid-cols-2 gap-3 mb-3">
            <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Case title" />
            <input value={field} onChange={(e) => setField(e.target.value)} placeholder="Field (e.g. machine learning)" />
          </div>
          <button className="btn" onClick={createCase} disabled={busy}>
            {busy ? "Creating case…" : "Create case from evaluation"}
          </button>
        </div>
      )}

      {loaded && cases.length === 0 && !evalId && (
        <div className="border border-[--rule] bg-white px-6 py-10 text-center">
          <p className="mb-4">No cases yet. Start with a free evaluation — it seeds your whole case.</p>
          <a className="btn" href="/#process">Get a free evaluation</a>
          <p className="docket-line mt-4 text-[#6b7570]">or</p>
          <button className="btn-quiet mt-2" onClick={createCase} disabled={busy}>Create an empty case</button>
        </div>
      )}

      <div className="grid gap-3">
        {cases.map((c) => (
          <a key={c.id} href={`/case/${c.id}`}
             className="border border-[--rule] bg-white px-6 py-4 flex justify-between items-center hover:border-[--docket] transition-colors">
            <div>
              <div style={{ fontFamily: "var(--font-serif), serif" }} className="text-lg">{c.title}</div>
              <div className="docket-line text-[#6b7570] mt-1">{c.field || "field not set"}</div>
            </div>
            <span className="docket-line text-[--docket]">Stage: {c.stage}</span>
          </a>
        ))}
      </div>
    </main>
  );
}

export default function Dashboard() {
  return (
    <Suspense>
      <DashboardInner />
    </Suspense>
  );
}
