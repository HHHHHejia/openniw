"use client";
import { useEffect, useRef, useState } from "react";
import { api, download, withToken } from "@/lib/api";
import { Header, FinishBar } from "@/components/session";

const DEGREE_LEVELS = ["doctorate", "master", "bachelor", "associate", "other"];
const DEGREE_COLS: [string, string][] = [
  ["level", "Level"], ["other_label", "Other label (if level=other)"],
  ["field", "Field of study"], ["institution", "Institution"],
  ["country", "Country"], ["month_year", "MM/YYYY"],
];
const FAMILY_COLS: [string, string][] = [
  ["family_name", "Family name"], ["given_name", "Given name"],
  ["middle_name", "Middle name"], ["dob", "DOB MM/DD/YYYY"],
  ["country_of_birth", "Country of birth"], ["relationship", "Relationship"],
];
const EMPLOYER_COLS: [string, string][] = [
  ["name", "Employer name"], ["address1", "Street address"],
  ["address2", "Address line 2"], ["city", "City"],
  ["state", "State"], ["postal_code", "Postal code"], ["country", "Country"],
  ["job_title", "Job title"], ["start", "Start MM/YYYY"],
  ["end", "End MM/YYYY (blank = current)"], ["hours_per_week", "Hours/week"],
];

function RowList({ value, onChange, cols, levelKey }: {
  value: any[]; onChange: (v: any[]) => void;
  cols: [string, string][]; levelKey?: string;
}) {
  const rows = Array.isArray(value) ? value : [];
  const set = (i: number, k: string, v: string) => {
    onChange(rows.map((r, j) => (j === i ? { ...r, [k]: v } : r)));
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
                <input value={row[k] || ""} onChange={(e) => set(i, k, e.target.value)}
                       disabled={k === "other_label" && levelKey === "level" && row.level !== "other"} />
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
  const [spec, setSpec] = useState<any>(null);
  const [answers, setAnswers] = useState<any>({});
  const [version, setVersion] = useState<number>(0);
  const [aiKeys, setAiKeys] = useState<Set<string>>(new Set());
  const [filled, setFilled] = useState<any[]>([]);
  const [section, setSection] = useState(0);
  const [busy, setBusy] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);
  const [conflict, setConflict] = useState(false);
  const [reports, setReports] = useState<Record<string, any>>({});
  const editedKeys = useRef<Set<string>>(new Set());

  const load = async () => {
    const [s, a, f] = await Promise.all([
      api("/api/forms/spec"), api("/api/forms/answers"), api("/api/forms/filled"),
    ]);
    setSpec(s);
    setAnswers(a.answers || {});
    setVersion(a.version || 0);
    setAiKeys(new Set(a.meta?.ai_keys || []));
    setFilled(f.filled || []);
    setConflict(false);
  };
  useEffect(() => { load().catch(() => {}); }, []);

  const setValue = (key: string, v: any) => {
    setAnswers((a: any) => ({ ...a, [key]: v }));
    editedKeys.current.add(key);
    setAiKeys((s) => {
      if (!s.has(key)) return s;
      const next = new Set(s);
      next.delete(key);
      return next;
    });
  };

  async function save(): Promise<boolean> {
    try {
      const res = await api("/api/forms/answers", {
        method: "PUT",
        body: { answers, base_version: version,
                edited_keys: Array.from(editedKeys.current) },
      });
      setVersion(res.version);
      editedKeys.current = new Set();
      setSaved(true);
      setTimeout(() => setSaved(false), 1500);
      return true;
    } catch (e: any) {
      if (e.status === 409) setConflict(true);
      return false;
    }
  }

  async function fill(code: string) {
    setBusy(code);
    try {
      if (!(await save())) return;
      const res = await api(`/api/forms/fill/${code}`, { method: "POST" });
      setReports((r) => ({ ...r, [code]: res.report }));
      setFilled((await api("/api/forms/filled")).filled || []);
    } finally {
      setBusy(null);
    }
  }

  if (!spec) return <p className="docket-line p-8">Loading forms…</p>;
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
    <div className="max-w-6xl mx-auto px-6 py-6">
      <Header active="forms" />
      <div className="flex items-center justify-between flex-wrap gap-3 mb-2">
        <h1 className="text-2xl" style={{ fontFamily: "var(--font-serif), serif" }}>
          Official forms — review & fill
        </h1>
        <button className="btn" onClick={save}>{saved ? "Saved ✓" : "Save answers"}</button>
      </div>
      {conflict && (
        <div className="border border-[--stamp] text-[--stamp] px-4 py-2 mb-4 flex items-center justify-between">
          <span className="docket-line">
            The answers file changed on disk (your agent may have edited it).
          </span>
          <button className="docket-line underline" onClick={() => load()}>
            Reload latest
          </button>
        </div>
      )}
      {aiKeys.size > 0 && (
        <p className="docket-line text-[#8a7a2a] mb-4">
          {aiKeys.size} fields were pre-filled by your agent — review each amber
          field; editing clears the mark.
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
                        <a className="docket-line text-[--docket] hover:underline"
                           href={withToken(`/api/forms/filled/${code}/pdf`)}
                           target="_blank" rel="noreferrer">
                          PDF ↗
                        </a>
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
              <div key={code} className="docket-line text-[#4f5a55] mt-2">
                {code}: {r.filled} fields filled
                {r.unmatched_fields?.length
                  ? ` · ${r.unmatched_fields.length} to hand-fill: ${r.unmatched_fields.join(", ")}`
                  : ""}
                {(r.warnings || []).map((w: string, i: number) => (
                  <div key={i} className="text-[--stamp]">{w}</div>
                ))}
              </div>
            ))}
            <p className="text-xs text-[#4f5a55] mt-3">
              Always PRINT the filled forms and verify every page on paper
              before signing.
            </p>
          </section>

          <section className="border border-[--docket] bg-[--field] px-5 py-4">
            <div className="docket-line text-[--docket] mb-2">Stage V — Filing package</div>
            <p className="text-sm mb-3">
              Filled forms + all drafted documents, zipped in lockbox order with
              fees and an assembly checklist.
            </p>
            <button className="btn w-full justify-center"
                    onClick={() => download("/api/forms/package", "openniw-package.zip")}>
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

      <FinishBar
        beforeFinish={async () => { await save(); }}
        summary={() => ({
          fields_edited: editedKeys.current.size,
          forms_filled: Object.keys(reports),
        })}
      />
    </div>
  );
}
