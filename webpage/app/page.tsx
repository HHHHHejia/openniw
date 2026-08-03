import { SiteNav, SiteFooter } from "@/components/nav";
import { CopyBlock } from "@/components/copy";

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
          free · open source (MIT) · not a law firm · not legal advice
        </div>
        <h1 className="text-4xl leading-tight mb-4"
            style={{ fontFamily: "var(--font-serif), serif" }}>
          An open-source <em>skill</em> for your NIW application.
        </h1>
        <div className="grid gap-2 text-lg text-[#333] leading-relaxed mb-6 max-w-2xl">
          <p>
            Install it into <b>Claude Code, Codex, or Cursor</b> — the AI
            you already have — and it organizes your <b>EB-2 NIW
            self-petition</b> end to end.
          </p>
          <p>
            <b>Everything stays in a folder on your computer.</b> No
            account, no cloud, no API keys.
          </p>
          <p>
            <b>Free, forever.</b> We charge nothing and provide no
            service — <b>you</b> prepare and file your own petition.
          </p>
        </div>
        <div className="flex gap-3 flex-wrap">
          <a href="/eval/" className="btn">Try the statistical evaluation — free, no sign-up</a>
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
            <b>It&apos;s a skill, not an app.</b> The whole thing is a folder
            of markdown instructions and small scripts that your agent
            reads — you can audit every line on GitHub in ten minutes.
          </li>
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
          <CopyBlock copyText="npx skills add HHHHHejia/openniw">npx skills add HHHHHejia/openniw</CopyBlock>
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
          <CopyBlock copyText={"mkdir my-niw && cd my-niw\nclaude"}
                     className="bg-[--field] border border-[--rule]">
            {"mkdir my-niw && cd my-niw\nclaude        # or your agent of choice\n> 帮我准备 NIW 申请   /   evaluate my NIW case"}
          </CopyBlock>
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

      {/* contribute + contact */}
      <section id="contribute" className="mb-12">
        <h2 className="text-2xl mb-2" style={{ fontFamily: "var(--font-serif), serif" }}>
          Help the next applicant
        </h2>
        <p className="text-sm text-[#4f5a55] mb-4 max-w-2xl">
          OpenNIW is a fully open-source, free, public-interest project
          (开源利益众生). It gets better through three kinds of contribution:
        </p>
        <div className="grid sm:grid-cols-3 gap-3 mb-4">
          <div className="border border-[--rule] bg-white px-4 py-4">
            <div className="docket-line text-[--docket] mb-2">Code</div>
            <p className="text-sm leading-relaxed">
              Issues and PRs welcome — form mappings, new browser pages,
              translations, anything on the{" "}
              <a className="text-[--docket] underline" target="_blank" rel="noreferrer"
                 href="https://github.com/HHHHHejia/openniw/issues">issue tracker</a>.
            </p>
          </div>
          <div className="border border-[--rule] bg-white px-4 py-4">
            <div className="docket-line text-[--docket] mb-2">Data points</div>
            <p className="text-sm leading-relaxed">
              Filed with or without us? Open an issue with your anonymized
              numbers and outcome (field, citations, timeline, RFE, result) —
              every real data point sharpens the benchmark for the next
              person.
            </p>
          </div>
          <div className="border border-[--rule] bg-white px-4 py-4">
            <div className="docket-line text-[--docket] mb-2">Attorneys</div>
            <p className="text-sm leading-relaxed">
              Prepare NIW cases professionally? Your frontier experience —
              what draws RFEs now, what wording holds up — can be folded
              into the playbooks. Credited or anonymous, your choice.
            </p>
          </div>
        </div>
        <p className="docket-line text-[#4f5a55]">
          Contact — WeChat: <span className="text-[--ink]">LittleGeng</span>
          {" · "}X:{" "}
          <a className="text-[--docket] underline" target="_blank" rel="noreferrer"
             href="https://x.com/hejia0530">x.com/hejia0530</a>
          {" · "}or{" "}
          <a className="text-[--docket] underline" target="_blank" rel="noreferrer"
             href="https://github.com/HHHHHejia/openniw/issues">GitHub issues</a>
        </p>
      </section>

      {/* prominent disclaimer */}
      <section className="border-2 border-[--stamp] bg-white px-6 py-5 mb-12">
        <div className="docket-line text-[--stamp] mb-2">Read this before you rely on anything here</div>
        <ul className="grid gap-1.5 text-sm text-[#333] leading-relaxed">
          <li>· <b>Completely free, open-source, public-interest.</b> No paid
            tier, no service, no upsell — ever.</li>
          <li>· <b>Your data never reaches us.</b> Your entire case is
            processed by <b>your own local AI</b> in a folder on <b>your
            computer</b>. We run no server that could even receive it; this
            website is static and nothing you type here leaves your browser.</li>
          <li>· <b>No liability for outcomes.</b> We are not attorneys and
            this is not legal advice. We accept no legal responsibility for
            the success or failure of any application — you prepare, review,
            sign, and file your own petition, and outcomes depend on your
            facts and adjudicator discretion.</li>
        </ul>
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
        <a href="/eval/" className="btn">Open the statistical evaluation →</a>
      </section>

      <SiteFooter />
    </div>
  );
}
