"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { api, withToken } from "@/lib/api";
import { Header, FinishBar } from "@/components/session";

// ---------------------------------------------------------------------------
// The guided card flow. One small card per screen; a docket-index rail shows
// the whole journey and allows free back/forward jumps. Any spec key not
// claimed by a card below is auto-collected into a per-section "More details"
// card, so new wizard-spec fields can never be silently lost.
// ---------------------------------------------------------------------------

type CardDef = {
  id: string;
  group: string;          // rail group label
  title: string;
  intro?: string;
  keys?: string[];        // scalar spec keys shown on this card
  kind?: "fields" | "degrees" | "employer" | "family" | "fill" | "package" | "finish";
  optional?: boolean;     // novice hint: safe to skip
};

const CARDS: CardDef[] = [
  { id: "name", group: "Identity", title: "Your legal name",
    intro: "Exactly as printed in your passport — this name flows onto every form.",
    keys: ["beneficiary.family_name", "beneficiary.given_name", "beneficiary.middle_name"] },
  { id: "native", group: "Identity", title: "Name in your native alphabet", optional: true,
    intro: "Only if your name is written in a non-Roman alphabet (中文, 한글, кириллица…). Otherwise just continue.",
    keys: ["native_name.family", "native_name.given", "native_name.middle"] },
  { id: "birth", group: "Identity", title: "Where and when you were born",
    keys: ["beneficiary.dob", "beneficiary.city_of_birth", "beneficiary.state_of_birth", "beneficiary.country_of_birth"] },
  { id: "gov", group: "Identity", title: "Citizenship & government numbers",
    intro: "Leave anything you don't have blank — never guess these.",
    keys: ["beneficiary.citizenship", "beneficiary.a_number", "beneficiary.ssn", "beneficiary.uscis_account"] },

  { id: "usaddr", group: "Contact", title: "Your U.S. mailing address",
    intro: "Where USCIS mails your notices. No P.O. boxes.",
    keys: ["mailing.street", "mailing.apt", "mailing.city", "mailing.state", "mailing.zip"] },
  { id: "intladdr", group: "Contact", title: "Address outside the U.S.?", optional: true,
    intro: "Only if your mailing address is not in the United States. Otherwise continue.",
    keys: ["mailing.province", "mailing.postal_code", "mailing.country"] },
  { id: "phone", group: "Contact", title: "Phone & email",
    intro: "USCIS texts the G-1145 acceptance notice to your mobile.",
    keys: ["contact.daytime_phone", "contact.mobile_phone", "contact.email"] },

  { id: "inus", group: "U.S. status", title: "Your arrival in the U.S.",
    keys: ["us_presence.in_us", "us_presence.date_of_arrival", "us_presence.i94_number"] },
  { id: "passport", group: "U.S. status", title: "Passport",
    keys: ["us_presence.passport_number", "us_presence.passport_country", "us_presence.passport_exp", "us_presence.travel_doc_number"] },
  { id: "status", group: "U.S. status", title: "Current status & history",
    keys: ["us_presence.current_status", "processing.prior_petition", "processing.in_proceedings"] },
  { id: "path", group: "U.S. status", title: "How you'll get the green card",
    intro: "Adjustment = file I-485 inside the U.S. later. Premium = USCIS decides the I-140 in 45 business days for an extra fee.",
    keys: ["processing.adjustment", "processing.premium", "processing.country_of_residence"] },
  { id: "consular", group: "U.S. status", title: "Consular processing details", optional: true,
    intro: "Only if you will interview at a U.S. consulate abroad instead of filing I-485.",
    keys: ["processing.consulate_city", "processing.consulate_country"] },
  { id: "abroad", group: "U.S. status", title: "Your address abroad",
    intro: "I-140 Part 4 asks for an address in your home country.",
    keys: ["foreign_address.street", "foreign_address.city", "foreign_address.province", "foreign_address.postal_code", "foreign_address.country"] },

  { id: "job", group: "Employment", title: "Your job",
    keys: ["employment.job_title", "employment.soc_code", "employment.soc_title"] },
  { id: "jobdesc", group: "Employment", title: "Describe the work — plainly",
    intro: "Under 200 characters, no employer or project names, emphasize research. An officer with no technical background reads this.",
    keys: ["employment.job_description"] },
  { id: "position", group: "Employment", title: "Position details",
    keys: ["employment.full_time", "employment.hours", "employment.permanent", "employment.new_position"] },
  { id: "pay", group: "Employment", title: "Compensation & occupation",
    keys: ["employment.wages", "employment.wages_per", "petitioner.occupation", "petitioner.annual_income"] },
  { id: "feeq", group: "Employment", title: "Two I-140 fee questions",
    intro: "As a self-petitioner YOU are the petitioner — answer for yourself. 'Small employer' (25 or fewer employees) sets the $300 Asylum Program Fee.",
    keys: ["petitioner.nonprofit", "petitioner.small_employer"] },

  { id: "degrees", group: "Education", title: "Your degrees", kind: "degrees",
    intro: "Highest first. Use the conferral date from the diploma." },
  { id: "employer", group: "Education", title: "Current employer", kind: "employer",
    intro: "For ETA-9089 Appendix A. Duties: 3–5 sentences, action verbs, no employer/advisor/grant names inside the text." },

  { id: "family", group: "Family", title: "Spouse & children", kind: "family",
    intro: "Spouse and ALL unmarried children under 21, whether or not they immigrate with you. No family? Just continue." },

  { id: "fill", group: "Generate & file", title: "Generate the official PDFs", kind: "fill" },
  { id: "package", group: "Generate & file", title: "Mailing & filing package", kind: "package" },
  { id: "finish", group: "Generate & file", title: "All set?", kind: "finish" },
];

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
  const set = (i: number, k: string, v: string) =>
    onChange(rows.map((r, j) => (j === i ? { ...r, [k]: v } : r)));
  return (
    <div className="grid gap-3">
      {rows.map((row, i) => (
        <div key={i} className="border border-[--rule] bg-[--field] p-4 grid sm:grid-cols-2 gap-3 relative">
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
          <button type="button" aria-label="Remove"
                  className="docket-line absolute top-2 right-3 text-[--stamp] hover:underline"
                  onClick={() => onChange(rows.filter((_, j) => j !== i))}>
            remove
          </button>
        </div>
      ))}
      <button type="button" className="btn-quiet !py-1.5 justify-self-start"
              onClick={() => onChange([...rows, {}])}>
        + Add {rows.length ? "another" : "one"}
      </button>
    </div>
  );
}

function EmployerForm({ value, onChange }: { value: any; onChange: (v: any) => void }) {
  const v = value && typeof value === "object" ? value : {};
  return (
    <div className="grid sm:grid-cols-2 gap-3">
      {EMPLOYER_COLS.map(([k, label]) => (
        <label key={k} className="text-xs">
          <span className="docket-line block mb-0.5 !text-[0.75rem]">{label}</span>
          <input value={v[k] || ""} onChange={(e) => onChange({ ...v, [k]: e.target.value })} />
        </label>
      ))}
      <label className="text-xs sm:col-span-2">
        <span className="docket-line block mb-0.5 !text-[0.75rem]">Job duties</span>
        <textarea rows={4} value={v.duties || ""}
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
  const [reports, setReports] = useState<Record<string, any>>({});
  const [step, setStep] = useState(0);
  const [busy, setBusy] = useState<string | null>(null);
  const [conflict, setConflict] = useState(false);
  const [railOpen, setRailOpen] = useState(false);
  const editedKeys = useRef<Set<string>>(new Set());
  const dirty = useRef(false);

  // ---- data ----------------------------------------------------------------
  const load = async () => {
    const [s, a, f] = await Promise.all([
      api("/api/forms/spec"), api("/api/forms/answers"), api("/api/forms/filled"),
    ]);
    setSpec(s); setAnswers(a.answers || {}); setVersion(a.version || 0);
    setAiKeys(new Set(a.meta?.ai_keys || []));
    setFilled(f.filled || []); setConflict(false);
  };
  useEffect(() => { load().catch(() => {}); }, []);

  const fieldByKey: Record<string, any> = useMemo(() => {
    const m: Record<string, any> = {};
    (spec?.sections || []).forEach((s: any) =>
      s.fields.forEach((f: any) => { m[f.key] = { ...f, section: s.title }; }));
    return m;
  }, [spec]);

  // cards + auto-fallback for any spec keys no card claims
  const cards: CardDef[] = useMemo(() => {
    if (!spec) return CARDS;
    const claimed = new Set<string>(
      CARDS.flatMap((c) => c.keys || []).concat(["degrees", "current_employer", "family"]));
    const extras: CardDef[] = [];
    (spec.sections || []).forEach((s: any) => {
      const missing = s.fields.map((f: any) => f.key).filter((k: string) => !claimed.has(k));
      if (missing.length)
        extras.push({ id: `more-${s.id}`, group: "More", title: `More: ${s.title}`, keys: missing });
    });
    const out = [...CARDS];
    const finishAt = out.findIndex((c) => c.kind === "fill");
    out.splice(finishAt, 0, ...extras);
    return out;
  }, [spec]);

  const card = cards[step];
  const groups = useMemo(() => {
    const g: { name: string; cards: number[] }[] = [];
    cards.forEach((c, i) => {
      const last = g[g.length - 1];
      if (!last || last.name !== c.group) g.push({ name: c.group, cards: [i] });
      else last.cards.push(i);
    });
    return g;
  }, [cards]);

  // ---- state helpers -------------------------------------------------------
  const setValue = (key: string, v: any) => {
    setAnswers((a: any) => ({ ...a, [key]: v }));
    editedKeys.current.add(key);
    dirty.current = true;
    setAiKeys((s) => {
      if (!s.has(key)) return s;
      const next = new Set(s); next.delete(key); return next;
    });
  };

  async function save(): Promise<boolean> {
    if (!dirty.current) return true;
    try {
      const res = await api("/api/forms/answers", {
        method: "PUT",
        body: { answers, base_version: version,
                edited_keys: Array.from(editedKeys.current) },
      });
      setVersion(res.version);
      editedKeys.current = new Set();
      dirty.current = false;
      return true;
    } catch (e: any) {
      if (e.status === 409) setConflict(true);
      return false;
    }
  }

  async function go(i: number) {
    await save();
    setStep(Math.max(0, Math.min(cards.length - 1, i)));
    setRailOpen(false);
    window.scrollTo({ top: 0 });
  }

  async function fill(code: string) {
    setBusy(code);
    try {
      if (!(await save())) return;
      const res = await api(`/api/forms/fill/${code}`, { method: "POST" });
      setReports((r) => ({ ...r, [code]: res.report }));
      setFilled((await api("/api/forms/filled")).filled || []);
    } finally { setBusy(null); }
  }

  // completeness per card (for the rail)
  const cardState = (c: CardDef): "done" | "partial" | "todo" => {
    if (c.kind === "degrees") return (answers.degrees || []).length ? "done" : "todo";
    if (c.kind === "employer")
      return answers.current_employer?.name ? "done" : "todo";
    if (c.kind === "family") return "done"; // optional by nature
    if (c.kind === "fill") return filled.length ? "done" : "todo";
    if (c.kind === "package" || c.kind === "finish") return "todo";
    const keys = c.keys || [];
    const req = keys.filter((k) => fieldByKey[k]?.required);
    const answered = (ks: string[]) =>
      ks.filter((k) => answers[k] !== undefined && answers[k] !== "").length;
    if (req.length && answered(req) === req.length) return "done";
    if (!req.length && answered(keys) > 0) return "done";
    return answered(keys) > 0 ? "partial" : "todo";
  };

  const amberLeft = useMemo(() => Array.from(aiKeys), [aiKeys]);
  const cardOfKey = (key: string) =>
    cards.findIndex((c) => (c.keys || []).includes(key)
      || (key === "degrees" && c.kind === "degrees")
      || (key === "current_employer" && c.kind === "employer")
      || (key === "family" && c.kind === "family"));

  if (!spec || !card) return <p className="docket-line p-8">Loading…</p>;

  // ---- field renderer ------------------------------------------------------
  function fieldControl(f: any) {
    const v = answers[f.key];
    if (f.type === "boolean") {
      return (
        <div className="flex gap-2">
          {[true, false].map((val) => (
            <button key={String(val)} type="button"
                    className={`docket-line px-5 py-2 border ${v === val ? "border-[--docket] text-[--docket] bg-white" : "border-[--rule] hover:border-[--ink]"}`}
                    onClick={() => setValue(f.key, val)}>
              {val ? "Yes" : "No"}
            </button>
          ))}
        </div>
      );
    }
    if (f.type === "textarea")
      return <textarea rows={4} value={v || ""} onChange={(e) => setValue(f.key, e.target.value)} />;
    return <input value={v || ""} onChange={(e) => setValue(f.key, e.target.value)} />;
  }

  function renderCardBody() {
    if (card.kind === "degrees")
      return <RowList value={answers.degrees} cols={DEGREE_COLS} levelKey="level"
                      onChange={(x) => setValue("degrees", x)} />;
    if (card.kind === "employer")
      return <EmployerForm value={answers.current_employer}
                           onChange={(x) => setValue("current_employer", x)} />;
    if (card.kind === "family")
      return <RowList value={answers.family} cols={FAMILY_COLS}
                      onChange={(x) => setValue("family", x)} />;
    if (card.kind === "fill") return renderFillCard();
    if (card.kind === "package") return renderPackageCard();
    if (card.kind === "finish") return renderFinishCard();
    return (
      <div className="grid gap-5">
        {(card.keys || []).map((k) => {
          const f = fieldByKey[k];
          if (!f) return null;
          const isAi = aiKeys.has(k);
          return (
            <div key={k} className={isAi ? "border-l-2 pl-3" : ""}
                 style={isAi ? { borderColor: "#8a7a2a" } : undefined}>
              <label className="block">
                <span className="docket-line mb-1.5 flex items-center gap-2">
                  {f.label}
                  {f.required && <span className="text-[--stamp]">*</span>}
                  {isAi && (
                    <span className="border px-1" style={{ color: "#8a7a2a", borderColor: "#8a7a2a" }}>
                      AI — please verify
                    </span>
                  )}
                </span>
                {fieldControl(f)}
                {f.help && <span className="block mt-1.5 text-xs text-[#4f5a55] leading-relaxed">{f.help}</span>}
              </label>
            </div>
          );
        })}
      </div>
    );
  }

  function renderFillCard() {
    return (
      <div className="grid gap-3">
        <p className="text-sm text-[#4f5a55]">
          Each button fills the real government PDF from your answers. Open
          each one and check it — then PRINT and verify on paper before
          signing.
        </p>
        {spec.forms.map((code: string) => {
          const f = filled.find((x: any) => x.form_code === code);
          const r = reports[code];
          return (
            <div key={code} className="border border-[--rule] bg-white px-4 py-3">
              <div className="flex items-center justify-between gap-2">
                <span className="docket-line">{code}</span>
                <div className="flex gap-3 items-center">
                  {f && (
                    <a className="docket-line text-[--docket] hover:underline"
                       href={withToken(`/api/forms/filled/${code}/pdf`)}
                       target="_blank" rel="noreferrer">open PDF ↗</a>
                  )}
                  <button className="btn-quiet !py-1 !px-3 docket-line" disabled={busy !== null}
                          onClick={() => fill(code)}>
                    {busy === code ? "…" : f ? "Refill" : "Fill"}
                  </button>
                </div>
              </div>
              {r && (
                <div className="docket-line text-[#4f5a55] mt-1.5">
                  {r.filled} fields filled
                  {r.unmatched_fields?.length
                    ? <> · hand-fill: <span className="text-[--stamp]">{r.unmatched_fields.join(", ")}</span></>
                    : " · nothing to hand-fill"}
                  {(r.warnings || []).map((w: string, i: number) => (
                    <div key={i} className="text-[--stamp]">{w}</div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    );
  }

  function renderPackageCard() {
    return (
      <div className="grid gap-4">
        <p className="text-sm text-[#4f5a55]">
          One ZIP with your filled forms, drafted documents as Word files, and
          a step-by-step assembly checklist in the exact order USCIS
          recommends.
        </p>
        <button className="btn justify-center"
                onClick={async () => {
                  const blob = (await api("/api/forms/package")) as Blob;
                  const url = URL.createObjectURL(blob);
                  const a = document.createElement("a");
                  a.href = url; a.download = "openniw-package.zip"; a.click();
                  URL.revokeObjectURL(url);
                }}>
          Download filing package
        </button>
        <div className="docket-line text-[#4f5a55]">
          Fees: I-140 ${spec.fees["i-140"]} + Asylum Program Fee ${spec.fees["asylum_program_fee_self"]} (self)
          {answers["processing.premium"] === true && <> + I-907 premium ${spec.fees["i-907_premium"]}</>}
        </div>
        {spec.filing_address && (
          <div className="border border-[--docket] bg-[--field] px-4 py-3">
            <div className="docket-line text-[--docket] mb-1">
              Mail to — {spec.filing_address.name}
            </div>
            <pre className="text-sm leading-relaxed whitespace-pre-wrap font-mono">{spec.filing_address.usps}</pre>
            <p className="text-xs text-[#4f5a55] mt-1.5">{spec.filing_address.note}</p>
          </div>
        )}
      </div>
    );
  }

  function renderFinishCard() {
    return (
      <div className="grid gap-4">
        {amberLeft.length > 0 ? (
          <div className="border px-4 py-3" style={{ borderColor: "#8a7a2a" }}>
            <div className="docket-line mb-2" style={{ color: "#8a7a2a" }}>
              {amberLeft.length} AI-filled {amberLeft.length === 1 ? "field" : "fields"} you haven&apos;t looked at yet
            </div>
            <div className="grid gap-1">
              {amberLeft.map((k) => (
                <button key={k} type="button"
                        className="docket-line text-left hover:underline"
                        onClick={() => go(cardOfKey(k))}>
                  → {fieldByKey[k]?.label || k}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <p className="docket-line text-[--docket]">
            Every AI-prefilled field has been reviewed. ✓
          </p>
        )}
        <p className="text-sm text-[#4f5a55]">
          Clicking Done saves everything and hands control back to your agent
          in the chat — it will walk you through printing, signing, and
          mailing. You can also come back here later.
        </p>
      </div>
    );
  }

  // ---- layout --------------------------------------------------------------
  const stepOfGroup = (gi: number) => groups.slice(0, gi).reduce((n, g) => n + g.cards.length, 0);

  const rail = (
    <nav className="w-60 shrink-0 border-r border-[--rule] pr-4 hidden lg:block sticky top-6 self-start max-h-[85vh] overflow-y-auto">
      {groups.map((g, gi) => (
        <div key={g.name} className="mb-4">
          <div className="docket-line text-[#4f5a55] mb-1.5">
            {String(gi + 1).padStart(2, "0")} · {g.name}
          </div>
          {g.cards.map((ci) => {
            const c = cards[ci];
            const st = cardState(c);
            const current = ci === step;
            return (
              <button key={c.id} type="button" onClick={() => go(ci)}
                      className={`flex items-center gap-2 w-full text-left text-sm py-1 px-2 -mx-2
                        ${current ? "bg-white border-l-2 border-[--docket]" : "hover:bg-white/60"}`}>
                <span className={`docket-line !text-[0.7rem] w-3 text-center shrink-0
                  ${st === "done" ? "text-[--docket]" : current ? "text-[--ink]" : "text-[#9aa39e]"}`}>
                  {st === "done" ? "✓" : current ? "●" : "○"}
                </span>
                <span className={current ? "text-[--ink]" : "text-[#4f5a55]"}>{c.title}</span>
              </button>
            );
          })}
        </div>
      ))}
    </nav>
  );

  return (
    <div className="max-w-5xl mx-auto px-6 py-6">
      <Header active="forms" />
      {conflict && (
        <div className="border border-[--stamp] text-[--stamp] px-4 py-2 mb-4 flex items-center justify-between">
          <span className="docket-line">The answers file changed on disk (your agent may have edited it).</span>
          <button className="docket-line underline" onClick={() => load()}>Reload latest</button>
        </div>
      )}

      {/* mobile: collapsible progress */}
      <div className="lg:hidden mb-4">
        <button className="btn-quiet w-full justify-between" onClick={() => setRailOpen(!railOpen)}>
          <span className="docket-line">Step {step + 1} of {cards.length} — {card.group}</span>
          <span>{railOpen ? "▲" : "▼"}</span>
        </button>
        {railOpen && (
          <div className="border border-[--rule] bg-white p-3 mt-1 grid gap-1">
            {cards.map((c, ci) => (
              <button key={c.id} className="docket-line text-left hover:underline"
                      onClick={() => go(ci)}>
                {cardState(c) === "done" ? "✓" : ci === step ? "●" : "○"} {c.title}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="flex gap-8">
        {rail}
        <main className="flex-1 max-w-xl">
          <div className="docket-line text-[#4f5a55] mb-2">
            Step {step + 1} of {cards.length}
            {card.optional && " · optional — skip if it doesn't apply"}
          </div>
          <h1 className="text-2xl mb-2" style={{ fontFamily: "var(--font-serif), serif" }}>
            {card.title}
          </h1>
          {card.intro && (
            <p className="text-sm text-[#4f5a55] mb-5 leading-relaxed">{card.intro}</p>
          )}

          <div className="border border-[--rule] bg-white px-6 py-6">
            {renderCardBody()}
          </div>

          <div className="flex items-center justify-between mt-5">
            <button className="btn-quiet" disabled={step === 0} onClick={() => go(step - 1)}>
              ← Back
            </button>
            {card.kind !== "finish" ? (
              <button className="btn" onClick={() => go(step + 1)}>
                Continue →
              </button>
            ) : <span />}
          </div>

          {card.kind === "finish" && (
            <FinishBar
              beforeFinish={async () => { await save(); }}
              summary={() => ({
                fields_edited: editedKeys.current.size,
                forms_filled: Object.keys(reports),
                ai_unreviewed: amberLeft.length,
              })}
            />
          )}
        </main>
      </div>
    </div>
  );
}
