"use client";
import { useEffect, useRef, useState } from "react";
import { api, uploadFile, withToken } from "@/lib/api";
import { Header, FinishBar } from "@/components/session";

// Stage I intake: every STANDARDIZABLE input lives here — links, file
// uploads (straight into sources/), and the fixed background questions.
// The non-standard work (fetching, reading, judging) happens back in the
// chat; this page hands the user back to the agent when it's done.

const DEGREES = ["PhD", "PhD in progress", "MD", "MD + PhD", "Master's",
                 "Bachelor's", "Other"];

type FileRow = { name: string; size: number; mtime: number };

function fmtSize(b: number): string {
  return b > 1048576 ? `${(b / 1048576).toFixed(1)} MB`
    : `${Math.max(1, Math.round(b / 1024))} KB`;
}

export default function IntakePage() {
  const [links, setLinks] = useState<Record<string, string>>({});
  const [basics, setBasics] = useState<Record<string, any>>({});
  const [files, setFiles] = useState<FileRow[]>([]);
  const [saved, setSaved] = useState(false);
  const [savedOnce, setSavedOnce] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadErr, setUploadErr] = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);

  useEffect(() => {
    api("/api/intake").then((r) => {
      setLinks(r.intake?.links || {});
      setBasics(r.intake?.basics || {});
      setFiles(r.files || []);
      if (r.version && r.version !== "0") setSavedOnce(true);
    }).catch(() => {});
  }, []);

  async function save() {
    await api("/api/intake", {
      method: "PUT", body: { intake: { links, basics } },
    });
    setSaved(true);
    setSavedOnce(true);
    setTimeout(() => setSaved(false), 1500);
  }

  async function doUpload(list: FileList | null) {
    if (!list || !list.length) return;
    setUploading(true);
    setUploadErr(null);
    try {
      for (const f of Array.from(list)) {
        const r = await uploadFile("/api/intake/upload", f);
        setFiles(r.files);
      }
    } catch (e: any) {
      setUploadErr(String(e.message || e));
    } finally {
      setUploading(false);
      if (fileInput.current) fileInput.current.value = "";
    }
  }

  const linksGiven = Object.values(links).some((v) => (v || "").trim());
  const basicsGiven = !!(basics.position && basics.degree);
  const steps = (linksGiven ? 1 : 0) + (files.length ? 1 : 0)
    + (basicsGiven ? 1 : 0) + (savedOnce ? 1 : 0);

  const linkField = (key: string, label: string, help: string,
                     placeholder: string) => (
    <label className="block">
      <span className="docket-line mb-1 block">{label}</span>
      <input value={links[key] || ""} placeholder={placeholder}
             onChange={(e) => setLinks({ ...links, [key]: e.target.value })}
             onBlur={() => { if (linksGiven) save(); }} />
      <span className="block mt-1 text-xs text-[#4f5a55]">{help}</span>
    </label>
  );

  return (
    <div className="max-w-2xl mx-auto px-6 py-6">
      <Header active="intake"
              progress={{
                label: savedOnce && steps >= 3
                  ? "intake complete — click Done below"
                  : `${steps} of 4 · links → files → basics → save`,
                done: steps, total: 4,
              }} />
      <h1 className="text-2xl mb-2" style={{ fontFamily: "var(--font-serif), serif" }}>
        Let&apos;s get to know your record
      </h1>
      <p className="text-sm text-[#4f5a55] mb-6 leading-relaxed">
        Give links where they exist and files where they don&apos;t. Your agent
        will fetch, read, and archive everything into your case folder — you
        never retype what a link can say.
      </p>

      {/* 1 — links */}
      <section className="border border-[--rule] bg-white px-6 py-5 mb-4">
        <div className="docket-line text-[--docket] mb-4">1 · Your links — paste, don&apos;t type lists</div>
        <div className="grid gap-4">
          {linkField("scholar_url", "Google Scholar profile",
            "The single highest-value link: publications, citations, h-index all come from here.",
            "https://scholar.google.com/citations?user=…")}
          {linkField("homepage_url", "Personal or lab homepage",
            "Bio, projects, news — anything public that tells your story.",
            "https://…")}
          {linkField("linkedin_url", "LinkedIn profile",
            "LinkedIn blocks robots — also upload its 'Save to PDF' export below so nothing is missed.",
            "https://www.linkedin.com/in/…")}
          <label className="block">
            <span className="docket-line mb-1 block">Other links — one per line</span>
            <textarea rows={2} value={links.other || ""}
                      placeholder={"https://github.com/…\nhttps://company.com/team/…"}
                      onChange={(e) => setLinks({ ...links, other: e.target.value })}
                      onBlur={() => { if (linksGiven) save(); }} />
            <span className="block mt-1 text-xs text-[#4f5a55]">
              GitHub, patents, press coverage, award pages…
            </span>
          </label>
        </div>
      </section>

      {/* 2 — files */}
      <section className="border border-[--rule] bg-white px-6 py-5 mb-4">
        <div className="docket-line text-[--docket] mb-2">2 · Your files — drop them here</div>
        <p className="text-xs text-[#4f5a55] mb-3">
          CV (PDF), LinkedIn &quot;Save to PDF&quot; export, and anything else useful
          (award letters, transcripts). They land in your case folder&apos;s
          <span className="font-mono"> sources/</span> — nothing leaves your computer.
        </p>
        <div
          className={`border-2 border-dashed px-6 py-8 text-center cursor-pointer
            ${dragOver ? "border-[--docket] bg-[--field]" : "border-[--rule]"}`}
          onClick={() => fileInput.current?.click()}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={(e) => { e.preventDefault(); setDragOver(false); doUpload(e.dataTransfer.files); }}>
          <span className="docket-line text-[#4f5a55]">
            {uploading ? "Uploading…" : "drag files here, or click to browse"}
          </span>
          <input ref={fileInput} type="file" multiple className="hidden"
                 onChange={(e) => doUpload(e.target.files)} />
        </div>
        {uploadErr && <p className="docket-line text-[--stamp] mt-2">{uploadErr}</p>}
        {files.length > 0 && (
          <div className="mt-3 grid gap-1">
            {files.map((f) => (
              <div key={f.name} className="flex justify-between text-sm border-t border-[--rule] pt-1">
                <span className="font-mono text-xs">{f.name}</span>
                <span className="docket-line text-[#4f5a55]">{fmtSize(f.size)} ✓</span>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* 3 — fixed basics */}
      <section className="border border-[--rule] bg-white px-6 py-5 mb-4">
        <div className="docket-line text-[--docket] mb-4">3 · Quick basics</div>
        <div className="grid sm:grid-cols-2 gap-4">
          <label className="block">
            <span className="docket-line mb-1 block">Current position</span>
            <input value={basics.position || ""} placeholder="e.g. Postdoctoral Fellow"
                   onChange={(e) => setBasics({ ...basics, position: e.target.value })}
                   onBlur={save} />
          </label>
          <label className="block">
            <span className="docket-line mb-1 block">Highest degree</span>
            <select value={basics.degree || ""}
                    onChange={(e) => { setBasics({ ...basics, degree: e.target.value }); }}>
              <option value="">—</option>
              {DEGREES.map((d) => <option key={d}>{d}</option>)}
            </select>
          </label>
          <label className="block">
            <span className="docket-line mb-1 block">Your field, in your words</span>
            <input value={basics.field || ""} placeholder="e.g. machine learning for drug discovery"
                   onChange={(e) => setBasics({ ...basics, field: e.target.value })}
                   onBlur={save} />
          </label>
          <div>
            <span className="docket-line mb-1 block">Currently in the U.S.?</span>
            <div className="flex gap-2">
              {[true, false].map((v) => (
                <button key={String(v)} type="button"
                        className={`docket-line px-5 py-2 border ${basics.in_us === v ? "border-[--docket] text-[--docket] bg-white" : "border-[--rule]"}`}
                        onClick={() => setBasics({ ...basics, in_us: v })}>
                  {v ? "Yes" : "No"}
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>

      <div className="flex items-center justify-between">
        <a className="docket-line text-[--docket] hover:underline"
           href={withToken("/benchmark/")}>
          optional: see how you compare with approved cases →
        </a>
        <button className="btn" onClick={save}>
          {saved ? "Saved ✓" : "Save"}
        </button>
      </div>

      <FinishBar
        stepId="intake"
        beforeFinish={save}
        summary={() => ({
          intake: {
            links: Object.fromEntries(
              Object.entries(links).filter(([, v]) => (v || "").trim())),
            files: files.map((f) => f.name),
            basics,
          },
        })}
      />
    </div>
  );
}
