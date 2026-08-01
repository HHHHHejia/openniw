"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api, downloadWithAuth } from "@/lib/api";

export default function FormsPage() {
  const { id } = useParams<{ id: string }>();
  const [spec, setSpec] = useState<any>(null);
  const [answers, setAnswers] = useState<any>({});
  const [filled, setFilled] = useState<any[]>([]);
  const [section, setSection] = useState(0);
  const [busy, setBusy] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);
  const [reports, setReports] = useState<Record<string, any>>({});

  const load = async () => {
    const [s, a, f] = await Promise.all([
      api(`/api/cases/${id}/forms/spec`),
      api(`/api/cases/${id}/forms/answers`),
      api(`/api/cases/${id}/forms/filled`),
    ]);
    setSpec(s);
    setAnswers(a.answers || {});
    setFilled(f);
  };
  useEffect(() => {
    load().catch(() => {});
  }, [id]);

  async function save() {
    await api(`/api/cases/${id}/forms/answers`, { method: "PUT", body: { answers } as any });
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  }

  async function prefill() {
    setBusy("prefill");
    try {
      const res = await api(`/api/cases/${id}/forms/prefill`, { method: "POST" });
      setAnswers(res.answers || {});
    } finally {
      setBusy(null);
    }
  }

  async function fill(code: string) {
    setBusy(code);
    try {
      await save();
      const res = await api(`/api/cases/${id}/forms/fill/${code}`, { method: "POST" });
      setReports((r) => ({ ...r, [code]: res.report }));
      setFilled(await api(`/api/cases/${id}/forms/filled`));
    } finally {
      setBusy(null);
    }
  }

  if (!spec) return <p className="docket-line">Loading forms…</p>;
  const sec = spec.sections[section];

  function field(f: any) {
    const v = answers[f.key];
    if (f.type === "boolean") {
      return (
        <div className="flex gap-2">
          {[true, false].map((val) => (
            <button key={String(val)}
                    className={`docket-line px-3 py-1.5 border ${v === val ? "border-[--docket] text-[--docket]" : "border-[--rule]"}`}
                    onClick={() => setAnswers({ ...answers, [f.key]: val })}>
              {val ? "Yes" : "No"}
            </button>
          ))}
        </div>
      );
    }
    if (f.type === "textarea") {
      return <textarea rows={3} value={v || ""} onChange={(e) => setAnswers({ ...answers, [f.key]: e.target.value })} />;
    }
    if (f.type === "degree_list" || f.type === "family_list" || f.type === "employer") {
      return (
        <textarea
          rows={5}
          className="font-mono !text-xs"
          value={typeof v === "string" ? v : JSON.stringify(v ?? (f.type === "employer" ? {} : []), null, 1)}
          onChange={(e) => {
            try {
              setAnswers({ ...answers, [f.key]: JSON.parse(e.target.value) });
            } catch {
              setAnswers({ ...answers, [f.key]: e.target.value });
            }
          }}
        />
      );
    }
    return <input value={v || ""} onChange={(e) => setAnswers({ ...answers, [f.key]: e.target.value })} />;
  }

  return (
    <div>
      <div className="flex items-center justify-between flex-wrap gap-3 mb-6">
        <h1 className="text-2xl" style={{ fontFamily: "var(--font-serif), serif" }}>
          Forms & package
        </h1>
        <div className="flex gap-2">
          <button className="btn-quiet" onClick={prefill} disabled={busy !== null}>
            {busy === "prefill" ? <span className="drafting-caret">Pre-filling</span> : "AI pre-fill from my record"}
          </button>
          <button className="btn" onClick={save}>{saved ? "Saved ✓" : "Save answers"}</button>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="flex gap-1 mb-4 flex-wrap">
            {spec.sections.map((s: any, i: number) => (
              <button key={s.id}
                      className={`docket-line px-3 py-1.5 border ${i === section ? "border-[--docket] text-[--docket]" : "border-[--rule] hover:border-[--ink]"}`}
                      onClick={() => setSection(i)}>
                {s.title}
              </button>
            ))}
          </div>
          <div className="border border-[--rule] bg-white px-5 py-5 grid gap-4">
            {sec.fields.map((f: any) => (
              <label key={f.key} className="text-sm">
                <span className="docket-line block mb-1">
                  {f.label}{f.required && <span className="text-[--stamp]"> *</span>}
                </span>
                {field(f)}
                {f.help && <span className="block mt-1 text-xs text-[#6b7570]">{f.help}</span>}
              </label>
            ))}
          </div>
        </div>

        <aside className="grid gap-5 content-start">
          <section className="border border-[--rule] bg-white px-5 py-4">
            <div className="docket-line mb-3">Generate official forms</div>
            <div className="grid gap-2">
              {spec.forms.map((code: string) => {
                const f = filled.find((x) => x.form_code === code);
                return (
                  <div key={code} className="flex items-center justify-between gap-2">
                    <span className="docket-line">{code}</span>
                    <div className="flex gap-2">
                      {f && (
                        <button className="docket-line text-[--docket] hover:underline"
                                onClick={() => downloadWithAuth(`/api/cases/${id}/forms/filled/${f.id}/pdf`, `${code}.pdf`)}>
                          PDF ↓
                        </button>
                      )}
                      <button className="btn-quiet !py-1 !px-2 docket-line" disabled={busy !== null}
                              onClick={() => fill(code)}>
                        {busy === code ? "…" : f ? "Refill" : "Fill"}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
            {Object.entries(reports).map(([code, r]: any) => (
              <p key={code} className="docket-line text-[#6b7570] mt-2">
                {code}: {r.filled} fields filled{r.unmatched_fields?.length ? `, ${r.unmatched_fields.length} unmatched` : ""}
              </p>
            ))}
          </section>

          <section className="border border-[--docket] bg-[--field] px-5 py-4">
            <div className="docket-line text-[--docket] mb-2">Stage V — Filing package</div>
            <p className="text-sm mb-3">
              Filled forms + all drafted documents, zipped in lockbox order with
              fees and an assembly checklist.
            </p>
            <button className="btn w-full justify-center"
                    onClick={() => downloadWithAuth(`/api/cases/${id}/forms/package`, "openniw-package.zip")}>
              Download package
            </button>
            <p className="docket-line text-[#6b7570] mt-3">
              Fees: I-140 ${spec.fees["i-140"]} + Asylum Program Fee ${spec.fees["asylum_program_fee_self"]}
              {" "}(self) · Premium optional ${spec.fees["i-907_premium"]}
            </p>
          </section>

          <p className="text-xs text-[#6b7570] leading-relaxed">{spec.lockbox_note}</p>
        </aside>
      </div>
    </div>
  );
}
