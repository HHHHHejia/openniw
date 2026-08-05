import { SiteNav, SiteFooter } from "@/components/nav";
import { CopyBlock } from "@/components/copy";

const STAGES: [string, string, string][] = [
  ["I", "Evaluate", "Paste your Google Scholar link. Your agent fetches your record, downloads your papers, benchmarks you against 7,458 approved cases, and gives an honest read — Dhanasar prong-by-prong (NIW) or criterion-by-criterion (EB-1A / O-1A)."],
  ["II·a", "Frame", "Compose and freeze the case frame — the canonical NIW endeavor sentence, the EB-1A field + claim frame, or the O-1 petitioner structure and itinerary scope. Every later document quotes it verbatim; rewording is a material-change risk."],
  ["II·b", "Evidence", "A personalized checklist plus the citation pipeline: every citing paper harvested, screened for independence, verified in full text, scored by depth of use — you pick the best ~10 in a browser page."],
  ["III", "Draft", "Support letters plus the petition letter in the shape officers expect — a Dhanasar three-prong brief (NIW), a Kazarian two-step brief with a Final Merits section (EB-1A), or the petitioner support letter + consultation package (O-1A) — every claim bound to an exhibit."],
  ["IV", "Forms", "NIW: a browser wizard verifies the 61-field answer set card by card and generates the real I-140 and companions. EB-1A / O-1A: precise field guides for the I-140 (E11) and I-129 — identity numbers are never guessed, in any category."],
  ["V", "Package", "A mock-officer red-team pass, then the filing package in USCIS-recommended assembly order — with current fees and the correct filing address for your category, state, and premium choice."],
  ["R", "RFE response", "If USCIS pushes back: upload the RFE letter and get a deadline-driven response workflow — diagnosis of every challenged point, an evidence-gap loop, fresh highlighted citation examples, new letters, a supplemental statement, and the assembled response package. Works even if your original petition wasn't prepared with OpenNIW."],
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
          Open-source <em>skills</em> for your NIW · EB-1A · O-1 · I-485
          application.
        </h1>
        <div className="grid gap-2 text-lg text-[#333] leading-relaxed mb-6 max-w-2xl">
          <p>
            Install them into <b>Claude Code, Codex, or Cursor</b> — the AI
            you already have — and they organize your <b>EB-2 NIW or
            EB-1A self-petition</b>, your <b>O-1A petition kit</b>, or the
            <b>employment-based I-485</b> that follows, end to end.
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
  │  your agent + an OpenNIW skill       │   the BRAIN — judgment,
  │  (niw/eb1a/o1/i485 · any major agent)│   drafting, conversation
  └──────┬─────────────────────┬─────────┘
 reads/   │                    │ opens at structured steps
 writes   ▼                    ▼
  ┌────────────┐   ┌──────────────────────────┐
  │ your case/ │◄──┤ local browser pages      │   the HANDS — intake,
  │ your files │   │ (run on 127.0.0.1 only)  │   benchmark, citation
  │ = the only │   │ + deterministic PDF fill │   picks, forms wizard
  │  storage   │   └──────────────────────────┘
  └────────────┘`}</pre>
        </div>
        <ul className="grid gap-2 text-[#333]">
          <li className="border-l-2 border-[--docket] pl-3">
            <b>They&apos;re skills, not an app.</b> The whole thing is a folder
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
          The workflow, stage by stage
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
        <p className="text-sm text-[#4f5a55] mt-3 leading-relaxed">
          <b>After the petition is approved:</b> the separate{" "}
          <span className="font-mono">i485-adjustment</span> skill handles the
          employment-based I-485 — eligibility gating, status-history
          assembly, the document checklist, and part-by-part form guidance for
          everyone in the family. It is deliberately an <b>assembly tool, not
          an eligibility tool</b>: it stops and sends you to a licensed
          attorney on inadmissibility questions, any criminal history, any
          overstay or unauthorized work, and the decision to actually use an
          EAD or advance parole.
        </p>
      </section>

      {/* install */}
      <section id="install" className="mb-12">
        <h2 className="text-2xl mb-4" style={{ fontFamily: "var(--font-serif), serif" }}>
          Install in one minute
        </h2>
        <div className="border border-[--docket] bg-[--field] px-6 py-5 mb-4">
          <div className="docket-line text-[--docket] mb-2">
            1 · Add the skills to your agent
          </div>
          <CopyBlock copyText="npx skills add HHHHHejia/openniw">npx skills add HHHHHejia/openniw</CopyBlock>
          <p className="text-xs text-[#4f5a55]">
            Works with Claude Code, Codex, Cursor and 70+ agents (when the
            installer asks, tick your agent — e.g. &quot;Claude Code&quot;). One
            command offers all four skills: <span className="font-mono">niw-petition</span>,{" "}
            <span className="font-mono">eb1a-petition</span> (beta),{" "}
            <span className="font-mono">o1-petition</span>,{" "}
            <span className="font-mono">i485-adjustment</span> (beta). Manual
            install: copy <span className="font-mono">.agents/skills/niw-petition</span>{" "}
            from the repo into <span className="font-mono">~/.claude/skills/</span>.
          </p>
        </div>
        <div className="border border-[--rule] bg-white px-6 py-5 mb-4">
          <div className="docket-line text-[--docket] mb-2">
            2 · Say the magic words
          </div>
          <CopyBlock copyText={"mkdir my-case && cd my-case\nclaude"}
                     className="bg-[--field] border border-[--rule]">
            {"mkdir my-case && cd my-case\nclaude        # or your agent of choice\n> 帮我准备 NIW 申请 / evaluate my EB-1A case / help me file my I-485"}
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
            fees (2026: I-140 $715 + $300 Asylum Program Fee for NIW /
            EB-1A self-petitions; O-1&apos;s I-129 $1,055 + an
            employer-size-based fee; optional premium processing $2,965)
            go to the government, not to us.
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
              Filed with or without us? Use the{" "}
              <a className="text-[--docket] underline" target="_blank" rel="noreferrer"
                 href="https://github.com/HHHHHejia/openniw/issues/new?template=data-point.yml">
                anonymous data-point form
              </a>{" "}
              (field, citations, timeline, RFE, result — no names, no case
              numbers) — every real data point sharpens the benchmark for
              the next person.
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
        <div className="border border-[--docket] bg-[--field] px-5 py-4 mb-4">
          <div className="docket-line text-[--docket] mb-1.5">
            EB-1A &amp; O-1A are here (beta) · OpenH1B — you&apos;re next
          </div>
          <p className="text-sm leading-relaxed">
            The <span className="font-mono">eb1a-petition</span> and{" "}
            <span className="font-mono">o1-petition</span> skills now ship
            in the same repo — built from USCIS primary sources,
            MIT-licensed open materials, and our approved-case dataset,
            not from firsthand filings. That&apos;s exactly why they need
            you: if you have actually been through an EB-1A or O-1 case —
            applicant or practitioner — reviewing their playbooks is the
            single most valuable contribution right now. And H1B (or any
            other category) is still waiting for its veteran: the whole
            framework is reusable. Reach out — let&apos;s build it together.
          </p>
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
