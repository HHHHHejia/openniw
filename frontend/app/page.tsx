"use client";
import { useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

const STEPS = [
  ["I", "Evaluate", "Paste your Google Scholar link. Get an honest, prong-by-prong read of your case in minutes — free."],
  ["II", "Collect", "The system pulls your publications, citations and record itself, then interviews you only for what it couldn't find."],
  ["III", "Draft", "Endeavor statement, petition letter, support letters — drafted in the structure real approved filings use, cited to your exhibits."],
  ["IV", "Forms", "I-140, ETA-9089 Appendix A, G-1145 filled programmatically from one wizard. No blank government PDFs."],
  ["V", "File", "A ZIP in lockbox order with fees, addresses and an assembly checklist. You print, sign, and mail."],
] as const;

export default function Landing() {
  const router = useRouter();
  const formRef = useRef<HTMLDivElement>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [fields, setFields] = useState({
    email: "",
    field: "",
    highest_degree: "",
    visa_status: "",
    scholar_url: "",
    homepage_url: "",
    linkedin_text: "",
    notes: "",
  });

  const set = (k: string) => (e: any) =>
    setFields((f) => ({ ...f, [k]: e.target.value }));

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      const form = new FormData();
      Object.entries(fields).forEach(([k, v]) => form.append(k, v));
      form.append("defer", "true");
      if (cvFile) form.append("cv", cvFile);
      const res = await api("/api/eval/free", { method: "POST", form });
      router.push(`/eval/${res.evaluation_id}?stream=1`);
    } catch (err: any) {
      setError(err.message);
      setBusy(false);
    }
  }

  return (
    <main>
      <header className="rule-b">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <span className="docket-line text-[--docket]">OpenNIW — Open Source NIW Preparation</span>
          <nav className="flex gap-4 items-center text-sm">
            <a className="hover:text-[--docket]" href="https://github.com/HHHHHejia/openniw" aria-label="Source code">Source</a>
            <a className="hover:text-[--docket]" href="/login">Sign in</a>
          </nav>
        </div>
      </header>

      {/* Hero: the endeavor sentence, as the document line it will become */}
      <section className="max-w-5xl mx-auto px-6 pt-20 pb-14">
        <p className="docket-line text-[--stamp] mb-6">Form I-140 · INA §203(b)(2)(B) · National Interest Waiver</p>
        <h1
          className="text-3xl sm:text-5xl leading-tight max-w-3xl"
          style={{ fontFamily: "var(--font-serif), Georgia, serif" }}
        >
          “My proposed endeavor is to{" "}
          <span className="border-b-2 border-[--docket] text-[--docket]">continue my research</span>{" "}
          in order to{" "}
          <span className="border-b-2 border-[--docket] text-[--docket]">serve the national interest</span>.”
        </h1>
        <p className="mt-8 max-w-2xl text-lg leading-relaxed">
          Every NIW petition stands on one sentence and the evidence behind it.
          OpenNIW builds both — from nothing more than your Google Scholar
          profile, homepage, or CV. It replicates the workflow of a full-service
          immigration firm, then automates away the paperwork they would have
          mailed you.
        </p>
        <div className="mt-8 flex gap-3 flex-wrap">
          <button className="btn" onClick={() => formRef.current?.scrollIntoView({ behavior: "smooth" })}>
            Get a free evaluation
          </button>
          <a className="btn-quiet" href="#process">See the five stages</a>
        </div>
        <p className="docket-line mt-6 text-[#6b7570]">
          Free · Open source (MIT) · Your data stays in your own deployment · Not legal advice
        </p>
      </section>

      {/* Process — roman numerals mirror the petition letter's own sections */}
      <section id="process" className="rule-b border-t border-[--rule] bg-[--field]">
        <div className="max-w-5xl mx-auto px-6 py-14 grid gap-8 sm:grid-cols-2 lg:grid-cols-5">
          {STEPS.map(([n, title, body]) => (
            <div key={n}>
              <div className="docket-line text-[--docket] mb-2">Stage {n}</div>
              <h3 className="text-lg mb-2" style={{ fontFamily: "var(--font-serif), serif" }}>{title}</h3>
              <p className="text-sm leading-relaxed text-[#3c4642]">{body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Free evaluation form */}
      <section ref={formRef} className="max-w-5xl mx-auto px-6 py-16">
        <div className="docket-line text-[--docket] mb-2">Stage I — Free Evaluation</div>
        <h2 className="text-2xl mb-2" style={{ fontFamily: "var(--font-serif), serif" }}>
          Give us links, not paperwork.
        </h2>
        <p className="text-sm text-[#3c4642] max-w-xl mb-8">
          One source is enough to start — the more you add, the sharper the
          evaluation. Nothing is shared; the report is yours.
        </p>
        <form onSubmit={submit} className="grid gap-4 max-w-2xl">
          <div className="grid sm:grid-cols-2 gap-4">
            <label className="text-sm">
              <span className="docket-line block mb-1">Email *</span>
              <input required type="email" value={fields.email} onChange={set("email")} placeholder="you@university.edu" />
            </label>
            <label className="text-sm">
              <span className="docket-line block mb-1">Research field</span>
              <input value={fields.field} onChange={set("field")} placeholder="e.g. machine learning" />
            </label>
            <label className="text-sm">
              <span className="docket-line block mb-1">Highest degree</span>
              <input value={fields.highest_degree} onChange={set("highest_degree")} placeholder="e.g. M.S. Computer Science" />
            </label>
            <label className="text-sm">
              <span className="docket-line block mb-1">Current U.S. status</span>
              <input value={fields.visa_status} onChange={set("visa_status")} placeholder="F-1 / OPT / H-1B / not in U.S." />
            </label>
          </div>
          <label className="text-sm">
            <span className="docket-line block mb-1">Google Scholar profile URL</span>
            <input value={fields.scholar_url} onChange={set("scholar_url")} placeholder="https://scholar.google.com/citations?user=..." />
          </label>
          <label className="text-sm">
            <span className="docket-line block mb-1">Personal homepage URL</span>
            <input value={fields.homepage_url} onChange={set("homepage_url")} placeholder="https://..." />
          </label>
          <label className="text-sm">
            <span className="docket-line block mb-1">CV (PDF)</span>
            <input type="file" accept=".pdf,.txt" onChange={(e) => setCvFile(e.target.files?.[0] || null)} className="!p-1.5" />
          </label>
          <label className="text-sm">
            <span className="docket-line block mb-1">LinkedIn — paste text or “Save to PDF” contents</span>
            <textarea rows={3} value={fields.linkedin_text} onChange={set("linkedin_text")} placeholder="LinkedIn blocks robots — paste your profile text here instead." />
          </label>
          <label className="text-sm">
            <span className="docket-line block mb-1">Anything else we should know</span>
            <textarea rows={2} value={fields.notes} onChange={set("notes")} placeholder="Awards, funding, patents, press, plans..." />
          </label>
          {error && <p className="text-sm text-[--stamp]">{error}</p>}
          <div>
            <button className="btn" disabled={busy}>
              {busy ? <span className="drafting-caret">Analyzing your record</span> : "Evaluate my case"}
            </button>
          </div>
          <p className="docket-line text-[#6b7570]">
            OpenNIW is a document preparation tool, not a law firm. The evaluation is informational, not legal advice.
          </p>
        </form>
      </section>

      <footer className="border-t border-[--rule]">
        <div className="max-w-5xl mx-auto px-6 py-8 flex flex-wrap gap-4 justify-between docket-line text-[#6b7570]">
          <span>OpenNIW · MIT License · 利益众生</span>
          <span>Built from the structure of real approved filings</span>
        </div>
      </footer>
    </main>
  );
}
