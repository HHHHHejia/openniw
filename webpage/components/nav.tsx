"use client";

export function SiteNav({ active }: { active: "home" | "eval" }) {
  return (
    <header className="border-b border-[--rule] mb-8 pb-3 flex items-end justify-between flex-wrap gap-3">
      <a href="/" className="hover:opacity-80">
        <span className="docket-line text-[--docket]">OpenNIW</span>
        <span className="text-xs text-[#4f5a55] ml-2">
          open source · free · your AI does the work
        </span>
      </a>
      <nav className="flex gap-1">
        <a href="/"
           className={`docket-line px-3 py-1.5 border ${active === "home" ? "border-[--docket] text-[--docket]" : "border-[--rule] hover:border-[--ink]"}`}>
          How it works
        </a>
        <a href="/eval/"
           className={`docket-line px-3 py-1.5 border ${active === "eval" ? "border-[--docket] text-[--docket]" : "border-[--rule] hover:border-[--ink]"}`}>
          Free benchmark
        </a>
        <a href="https://github.com/HHHHHejia/openniw" target="_blank" rel="noreferrer"
           className="docket-line px-3 py-1.5 border border-[--rule] hover:border-[--ink]">
          GitHub ↗
        </a>
      </nav>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="border-t border-[--rule] mt-12 pt-4 pb-8">
      <p className="text-xs text-[#4f5a55] leading-relaxed max-w-2xl">
        OpenNIW is a free, open-source (MIT) document-preparation and
        self-help tool — not a law firm, and not legal advice. Immigration
        outcomes depend on individual facts and adjudicator discretion;
        review everything before filing and consider consulting a licensed
        attorney. Benchmark data is aggregated from publicly posted approval
        notices (public-approval-source, 2012–2026), self-reported by the law firm and
        successful cases only — it shows distributions of approved profiles,
        never an individual&apos;s approval probability. This site is fully
        static: no accounts, no cookies, no tracking, nothing you type here
        leaves your browser. 开源利益众生.
      </p>
    </footer>
  );
}
