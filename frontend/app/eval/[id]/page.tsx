"use client";
import { Suspense, useEffect, useRef, useState } from "react";
import { useParams, useSearchParams } from "next/navigation";
import Md from "@/components/Md";
import { api, downloadUrl, getToken } from "@/lib/api";

const TIER_COPY: Record<string, [string, string]> = {
  strong: ["STRONG CASE", "#1f6f54"],
  promising: ["PROMISING CASE", "#1f6f54"],
  borderline: ["BORDERLINE — STRENGTHEN FIRST", "#b3402a"],
  "not-yet": ["NOT YET — BUILD THE RECORD", "#b3402a"],
};

const STAGE_COPY: Record<string, string> = {
  fetching: "Fetching your public record",
  profiling: "Consolidating your profile",
  evaluating: "Applying the Dhanasar framework — the report writes itself below",
};

function ProngBars({ scores }: { scores: any }) {
  if (!scores || !Object.keys(scores).length) return null;
  const items: [string, string][] = [
    ["prong1", "Prong 1 · merit & national importance"],
    ["prong2", "Prong 2 · well positioned"],
    ["prong3", "Prong 3 · balance favors waiver"],
  ];
  return (
    <div className="grid gap-2 px-6 py-4 rule-b">
      {items.map(([k, label]) => {
        const v = scores[k] ?? 0;
        return (
          <div key={k} className="flex items-center gap-3">
            <span className="docket-line w-64 shrink-0">{label}</span>
            <div className="flex gap-1" role="img" aria-label={`${label}: ${v} of 5`}>
              {[1, 2, 3, 4, 5].map((i) => (
                <span key={i} className="inline-block w-6 h-2.5 border border-[--rule]"
                      style={{ background: i <= v ? (v >= 3 ? "var(--docket)" : "var(--stamp)") : "transparent" }} />
              ))}
            </div>
            <span className="docket-line text-[#6b7570]">{v}/5</span>
          </div>
        );
      })}
    </div>
  );
}

function EvalInner() {
  const { id } = useParams<{ id: string }>();
  const search = useSearchParams();
  const wantStream = search.get("stream") === "1";
  const [report, setReport] = useState("");
  const [stage, setStage] = useState<string>("");
  const [tier, setTier] = useState<string | null>(null);
  const [scores, setScores] = useState<any>(null);
  const [done, setDone] = useState(false);
  const [error, setError] = useState("");
  const started = useRef(false);

  useEffect(() => {
    if (started.current) return;
    started.current = true;

    async function consumeStream() {
      try {
        const res = await fetch(downloadUrl(`/api/eval/${id}/stream`));
        if (!res.ok || !res.body) throw new Error("stream unavailable");
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buf = "";
        for (;;) {
          const { value, done: end } = await reader.read();
          if (end) break;
          buf += decoder.decode(value, { stream: true });
          const events = buf.split("\n\n");
          buf = events.pop() || "";
          for (const ev of events) {
            const line = ev.split("\n").find((l) => l.startsWith("data: "));
            if (!line) continue;
            const data = JSON.parse(line.slice(6));
            if (data.delta) setReport((r) => r + data.delta);
            if (data.stage) setStage(data.stage);
            if (data.report_md) setReport(data.report_md);
            if (data.tier) setTier(data.tier);
            if (data.prong_scores) setScores(data.prong_scores);
            if (data.stage === "done") setDone(true);
            if (data.stage === "error") setError(data.error || "Evaluation failed");
          }
        }
      } catch {
        pollFallback();
      }
    }

    async function pollFallback() {
      for (let i = 0; i < 240; i++) {
        try {
          const data = await api(`/api/eval/${id}`);
          if (data.status === "done") {
            setReport(data.report_md || "");
            setTier(data.tier);
            setScores(data.prong_scores);
            setDone(true);
            return;
          }
        } catch (e: any) {
          setError(e.message);
          return;
        }
        await new Promise((r) => setTimeout(r, 3000));
      }
    }

    if (wantStream) consumeStream();
    else pollFallback();
  }, [id, wantStream]);

  const tierBadge = tier ? TIER_COPY[tier] || [tier.toUpperCase(), "#16211e"] : null;

  return (
    <main className="max-w-3xl mx-auto px-6 py-12">
      <a href="/" className="docket-line text-[--docket]">← OpenNIW</a>
      <div className="mt-8 border border-[--rule] bg-white">
        <div className="rule-b px-6 py-4 flex items-center justify-between flex-wrap gap-2">
          <span className="docket-line">Free Evaluation — Report</span>
          {tierBadge && (
            <span className="docket-line px-2 py-1 border" style={{ color: tierBadge[1], borderColor: tierBadge[1] }}>
              {tierBadge[0]}
            </span>
          )}
        </div>
        {done && <ProngBars scores={scores} />}
        <div className="px-6 py-6">
          {error && <p className="text-[--stamp] text-sm">{error}</p>}
          {!error && !done && !report && (
            <div className="py-14 text-center">
              <p className="drafting-caret text-lg" style={{ fontFamily: "var(--font-serif), serif" }}>
                {STAGE_COPY[stage] || "Reading your record"}
              </p>
              <p className="docket-line mt-3 text-[#6b7570]">
                fetch sources · consolidate profile · apply the Dhanasar framework
              </p>
            </div>
          )}
          {report && (
            <div>
              <Md>{report}</Md>
              {!done && !error && <p className="drafting-caret docket-line text-[--docket] mt-2">writing</p>}
            </div>
          )}
        </div>
      </div>
      {done && (
        <div className="mt-8 border border-[--docket] bg-[--field] px-6 py-6">
          <div className="docket-line text-[--docket] mb-2">Next — Stage II</div>
          <p className="text-sm mb-4">
            Turn this evaluation into a case: OpenNIW seeds your evidence
            checklist from this report and starts collecting automatically.
          </p>
          <a className="btn" href={getToken() ? `/dashboard?eval=${id}` : `/login?eval=${id}`}>
            Start my case
          </a>
        </div>
      )}
    </main>
  );
}

export default function EvalResult() {
  return (
    <Suspense>
      <EvalInner />
    </Suspense>
  );
}
