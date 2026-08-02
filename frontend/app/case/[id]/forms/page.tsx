"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api, downloadWithAuth } from "@/lib/api";

const DEGREE_LEVELS = ["doctorate", "master", "bachelor", "associate", "other"];
const DEGREE_COLS: [string, string][] = [
  ["level", "Level"], ["field", "Field of study"], ["institution", "Institution"],
  ["country", "Country"], ["month_year", "MM/YYYY"],
];
const FAMILY_COLS: [string, string][] = [
  ["family_name", "Family name"], ["given_name", "Given name"],
  ["dob", "DOB MM/DD/YYYY"], ["country_of_birth", "Country of birth"],
  ["relationship", "Relationship"],
];
const EMPLOYER_COLS: [string, string][] = [
  ["name", "Employer name"], ["address1", "Street address"], ["city", "City"],
  ["state", "State"], ["postal_code", "Postal code"], ["country", "Country"],
  ["job_title", "Job title"], ["start", "Start MM/YYYY"],
  ["hours_per_week", "Hours/week"],
];

function RowList({ value, onChange, cols, levelKey }: {
  value: any[]; onChange: (v: any[]) => void;
  cols: [string, string][]; levelKey?: string;
}) {
  const rows = Array.isArray(value) ? value : [];
  const set = (i: number, k: string, v: string) => {
    const next = rows.map((r, j) => (j === i ? { ...r, [k]: v } : r));
    onChange(next);
  };
  return (
    <div className="grid gap-2">
      {rows.map((row, i) => (
        <div key={i} className="border border-[--rule] bg-[--field] p-3 grid sm:grid-cols-3 gap-2 relative">
          {cols.map(([k, label]) => (
            <label key={k} className="text-xs">
              <span className="docket-line block mb-0.5 !text-[0.75rem]">{label}</span>
              {k === levelKey ? (
                <select value={row[k] || ""} onChange={(e) => set(i, k, e.target.value)}>
                  <option value="">—</option>
                  {DEGREE_LEVELS.map((l) => <option key={l} value={l}>{l}</option>)}
                </select>
              ) : (
                <input value={row[k] || ""} onChange={(e) => set(i, k, e.target.value)} />
              )}
            </label>
          ))}
          <button type="button" aria-label="Remove row"
                  className="docket-line absolute top-2 right-2 text-[--stamp] hover:underline"
                  onClick={() => onChange(rows.filter((_, j) => j !== i))}>
            remove
          </button>
        </div>
      ))}
      <button type="button" className="btn-quiet !py-1.5 justify-self-start"
              onClick={() => onChange([...rows, {}])}>
        + Add
      </button>
    </div>
  );
}

function EmployerForm({ value, onChange }: { value: any; onChange: (v: any) => void }) {
  const v = value && typeof value === "object" ? value : {};
  return (
    <div className="border border-[--rule] bg-[--field] p-3 grid sm:grid-cols-3 gap-2">
      {EMPLOYER_COLS.map(([k, label]) => (
        <label key={k} className="text-xs">
          <span className="docket-line block mb-0.5 !text-[0.75rem]">{label}</span>
          <input value={v[k] || ""} onChange={(e) => onChange({ ...v, [k]: e.target.value })} />
        </label>
      ))}
      <label className="text-xs sm:col-span-3">
        <span className="docket-line block mb-0.5 !text-[0.75rem]">
          Job duties — 3–5 sentences, action verbs; no employer/advisor/grant names inside
        </span>
        <textarea rows={3} value={v.duties || ""}
                  onChange={(e) => onChange({ ...v, duties: e.target.value })} />
      </label>
    </div>
  );
}

export default function FormsPage() {
  const { id } = useParams<{ id: string }>();
  const [spec, setSpec] = useState<any>(null);
  const [answers, setAnswers] = useState<any>({});
  const [aiKeys, setAiKeys] = useState<Set<string>>(new Set());
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

  const setValue = (key: string, v: any) => {
    setAnswers((a: any) => ({ ...a, [key]: v }));
    setAiKeys((s) => {
      if (!s.has(key)) return s;
      const next = new Set(s);
      next.delete(key);
      return next;
    });
  };

  async function save() {
    await api(`/api/cases/${id}/forms/answers`, { method: "PUT", body: { answers } as any });
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  }

  async function prefill() {
    setBusy("prefill");
    try {
      const before = { ...answers };
      const res = await api(`/api/cases/${id}/forms/prefill`, { method: "POST" });
      const next = res.answers || {};
      const marked = new Set<string>();
      Object.keys(next).forEach((k) => {
        if (before[k] === undefined && next[k] !== undefined) marked.add(k);
      });
      setAnswers(next);
      setAiKeys(marked);
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
            <button key={String(val)} type="button"
                    className={`docket-line px-3 py-1.5 border ${v === val ? "border-[--docket] text-[--docket]" : "border-[--rule]"}`}
                    onClick={() => setValue(f.key, val)}>
              {val ? "Yes" : "No"}
            </button>
          ))}
        </div>
      );
    }
    if (f.type === "textarea") {
      return <textarea rows={3} value={v || ""} onChange={(e) => setValue(f.key, e.target.value)} />;
    }
    if (f.type === "degree_list") {
      return <RowList value={v} onChange={(x) => setValue(f.key, x)} cols={DEGREE_COLS} levelKey="level" />;
    }
    if (f.type === "family_list") {
      return <RowList value={v} onChange={(x) => setValue(f.key, x)} cols={FAMILY_COLS} />;
    }
    if (f.type === "employer") {
      return <EmployerForm value={v} onChange={(x) => setValue(f.key, x)} />;
    }
    return <input value={v || ""} onChange={(e) => setValue(f.key, e.target.value)} />;
  }

  return (
    <div>
      <div className="flex items-center justify-between flex-wrap gap-3 mb-2">
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
      {aiKeys.size > 0 && (
        <p className="docket-line text-[#8a7a2a] mb-4">
          {aiKeys.size} fields pre-filled by AI — review each amber field; editing clears the mark.
        </p>
      )}

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
              <div key={f.key} className={aiKeys.has(f.key) ? "border-l-2 pl-3" : ""}
                   style={aiKeys.has(f.key) ? { borderColor: "#8a7a2a" } : undefined}>
                <label className="text-sm">
                  <span className="docket-line mb-1 flex items-center gap-2">
                    {f.label}{f.required && <span className="text-[--stamp]">*</span>}
                    {aiKeys.has(f.key) && (
                      <span className="border px-1" style={{ color: "#8a7a2a", borderColor: "#8a7a2a" }}>AI</span>
                    )}
                  </span>
                  {field(f)}
                  {f.help && <span className="block mt-1 text-xs text-[#4f5a55]">{f.help}</span>}
                </label>
              </div>
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
              <p key={code} className="docket-line text-[#4f5a55] mt-2">
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
            <p className="docket-line text-[#4f5a55] mt-3">
              Fees: I-140 ${spec.fees["i-140"]} + Asylum Program Fee ${spec.fees["asylum_program_fee_self"]}
              {" "}(self) · Premium optional ${spec.fees["i-907_premium"]}
            </p>
            {spec.filing_address && (
              <div className="mt-3 border-t border-[--docket] pt-3">
                <div className="docket-line text-[--docket] mb-1">
                  Mail to — {spec.filing_address.name}
                </div>
                <pre className="text-xs leading-relaxed whitespace-pre-wrap font-mono">
                  {spec.filing_address.usps}
                </pre>
                <p className="text-xs text-[#4f5a55] mt-1">{spec.filing_address.note}</p>
              </div>
            )}
          </section>

          <p className="text-xs text-[#4f5a55] leading-relaxed">{spec.lockbox_note}</p>
        </aside>
      </div>
    </div>
  );
}
