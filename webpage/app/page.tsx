import { SiteNav, SiteFooter } from "@/components/nav";

const STAGES: [string, string, string][] = [
  ["I", "Evaluate", "Paste your Google Scholar link. Your agent fetches your record, downloads your papers, benchmarks you against 7,458 approved cases, and gives an honest, prong-by-prong read."],
  ["II·a", "Endeavor", "Compose and freeze the one canonical endeavor sentence — every document quotes it verbatim, because USCIS treats rewording as a material-change risk."],
  ["II·b", "Evidence", "A personalized checklist plus the citation pipeline: every citing paper harvested, screened for independence, verified in full text, scored by depth of use — you pick the best ~10 in a browser page."],
  ["III", "Draft", "Proposed Endeavor Statement → support letters → the Petition Letter (a Dhanasar three-prong brief, every claim bound to an exhibit) → Index of Exhibits."],
  ["IV", "Forms", "Your agent pre-fills the official PDFs' 61-field answer set (never guessing identity numbers), then opens a browser wizard: verify amber AI fields card by card, generate the real I-140 and companions, inspect them live."],
  ["V", "Package", "A twelve-rule mock-officer pass, then the ZIP in USCIS-recommended assembly order with fees and the correct lockbox address picked by your state and premium choice."],
];

export default function Landing() {
  return (
    <div className="max-w-3xl mx-auto px-6 py-6">
      <SiteNav active="home" />

      {/* hero */}
      <section className="mb-12">
        <div className="docket-line text-[--docket] mb-3">
          free · open source (MIT) · no accounts · no API keys · not a law
          firm · not legal advice
        </div>
        <h1 className="text-4xl leading-tight mb-4"
            style={{ fontFamily: "var(--font-serif), serif" }}>
          Organize your NIW self-petition faster — with the AI you
          already have.
        </h1>
        <p className="text-lg text-[#333] leading-relaxed mb-2 max-w-2xl">
          OpenNIW is a free tool that helps you structure and speed up your
          own EB-2 National Interest Waiver paperwork, using the coding
          agent you already pay for — Claude Code, Codex, Cursor. The whole
          preparation workflow runs in a folder on your computer:
          evaluation, evidence, drafting, official forms, filing package.
        </p>
        <p className="text-lg text-[#333] leading-relaxed mb-6 max-w-2xl">
          We charge nothing and provide no service — you prepare and file
          your own petition; we just built the tool.
        </p>
        <div className="flex gap-3 flex-wrap">
          <a href="/eval/" className="btn">Try the free benchmark — no sign-up</a>
          <a href="#install" className="btn-quiet">Install the skill</a>
        </div>
      </section>

      {/* what it is */}
      <section className="mb-12">
        <h2 className="text-2xl mb-4" style={{ fontFamily: "var(--font-serif), serif" }}>
          How it works
        </h2>
        <div className="border border-[--rule] bg-white px-6 py-5 mb-4">
          <pre className="text-xs leading-relaxed overflow-x-auto font-mono text-[#333]">{`
  ┌──────────────────────────────────────┐
  │  your agent + the niw-petition skill │   the BRAIN — judgment,
  │  (Claude Code / Codex / Cursor …)    │   drafting, conversation
  └──────┬─────────────────────┬─────────┘
 reads/   │                    │ opens at structured steps
 writes   ▼                    ▼
  ┌────────────┐   ┌──────────────────────────┐
  │ niw-case/  │◄──┤ local browser pages      │   the HANDS — intake,
  │ your files │   │ (run on 127.0.0.1 only)  │   benchmark, citation
  │ = the only │   │ + deterministic PDF fill │   picks, forms wizard
  │  storage   │   └──────────────────────────┘
  └────────────┘`}</pre>
        </div>
        <ul className="grid gap-2 text-[#333]">
          <li className="border-l-2 border-[--docket] pl-3">
            <b>No accounts, no cloud, no API keys.</b> Your case lives in a
            folder you own; the AI is your existing agent subscription;
            browser pages run on localhost only.
          </li>
          <li className="border-l-2 border-[--docket] pl-3">
            <b>Standardized inputs in the browser, judgment in the chat.</b>{" "}
            Links, uploads, fixed questions, and 61 form fields get proper
            UI; evaluation and drafting stay conversational.
          </li>
          <li className="border-l-2 border-[--docket] pl-3">
            <b>Built from real filings.</b> Templates distilled from
            professionally prepared petitions and a real RFE cycle
            (de-identified), with twelve RFE-prevention rules baked in.
          </li>
          <li className="border-l-2 border-[--docket] pl-3">
            <b>Survives weeks of short sessions.</b> A STATE.md working file
            means any session — even a browser tab left open overnight —
            resumes exactly where you stopped.
          </li>
        </ul>
      </section>

      {/* five stages */}
      <section className="mb-12">
        <h2 className="text-2xl mb-4" style={{ fontFamily: "var(--font-serif), serif" }}>
          The six stages
        </h2>
        <div className="grid gap-2">
          {STAGES.map(([num, name, desc]) => (
            <div key={num} className="border border-[--rule] bg-white px-5 py-4 flex gap-4">
              <div className="docket-line text-[--docket] w-10 shrink-0 pt-0.5">{num}</div>
              <div>
                <div className="docket-line mb-1">{name}</div>
                <p className="text-sm text-[#333] leading-relaxed">{desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* install */}
      <section id="install" className="mb-12">
        <h2 className="text-2xl mb-4" style={{ fontFamily: "var(--font-serif), serif" }}>
          Install in one minute
        </h2>
        <div className="border border-[--docket] bg-[--field] px-6 py-5 mb-4">
          <div className="docket-line text-[--docket] mb-2">
            1 · Add the skill to your agent
          </div>
          <pre className="bg-white border border-[--rule] px-4 py-3 text-sm font-mono overflow-x-auto mb-2">npx skills add HHHHHejia/openniw</pre>
          <p className="text-xs text-[#4f5a55]">
            Works with Claude Code, Codex, Cursor and 70+ agents (when the
            installer asks, tick your agent — e.g. &quot;Claude Code&quot;). Manual
            install: copy <span className="font-mono">.agents/skills/niw-petition</span>{" "}
            from the repo into <span className="font-mono">~/.claude/skills/</span>.
          </p>
        </div>
        <div className="border border-[--rule] bg-white px-6 py-5 mb-4">
          <div className="docket-line text-[--docket] mb-2">
            2 · Say the magic words
          </div>
          <pre className="bg-[--field] border border-[--rule] px-4 py-3 text-sm font-mono overflow-x-auto mb-2">mkdir my-niw && cd my-niw
claude        # or your agent of choice
&gt; 帮我准备 NIW 申请   /   evaluate my NIW case</pre>
          <p className="text-xs text-[#4f5a55]">
            The skill opens a browser intake page for your links and files,
            then your agent takes it from there — stage by stage, resumable
            anytime. A small helper (<span className="font-mono">pip install openniw</span>)
            is installed automatically for the browser pages and PDF filling.
          </p>
        </div>
        <div className="border border-[--rule] bg-white px-6 py-5">
          <div className="docket-line text-[--docket] mb-2">
            3 · What it costs
          </div>
          <p className="text-sm text-[#333] leading-relaxed">
            Nothing, beyond what you already pay: the project is MIT-licensed
            and the AI is your own subscription. Your actual USCIS filing
            fees (2026: I-140 $715 + $300 Asylum Program Fee; optional
            premium processing $2,965) go to the government, not to us.
          </p>
        </div>
      </section>

      {/* free eval CTA */}
      <section className="border border-[--docket] bg-white px-6 py-6 text-center">
        <h2 className="text-xl mb-2" style={{ fontFamily: "var(--font-serif), serif" }}>
          Not sure you qualify? Look at the data first.
        </h2>
        <p className="text-sm text-[#4f5a55] mb-4 max-w-lg mx-auto">
          Compare your citations and papers against 7,458 publicly posted
          approved cases — by field, over time, with processing-time
          simulation. Runs entirely in your browser; nothing you type leaves
          your machine.
        </p>
        <a href="/eval/" className="btn">Open the free benchmark →</a>
      </section>

      <SiteFooter />
    </div>
  );
}
