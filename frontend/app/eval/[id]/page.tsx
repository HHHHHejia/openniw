"use client";
import { useEffect, useState } from "react";
import { useParams, useSearchParams } from "next/navigation";
import Md from "@/components/Md";
import { api, getToken } from "@/lib/api";

const TIER_COPY: Record<string, [string, string]> = {
  strong: ["STRONG CASE", "#1f6f54"],
  promising: ["PROMISING CASE", "#1f6f54"],
  borderline: ["BORDERLINE — STRENGTHEN FIRST", "#b3402a"],
  "not-yet": ["NOT YET — BUILD THE RECORD", "#b3402a"],
};

export default function EvalResult() {
  const { id } = useParams<{ id: string }>();
  const search = useSearchParams();
  const [ev, setEv] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let stop = false;
    async function poll() {
      for (let i = 0; i < 240 && !stop; i++) {
        try {
          const data = await api(`/api/eval/${id}`);
          if (stop) return;
          setEv(data);
          if (data.status === "done") return;
        } catch (e: any) {
          setError(e.message);
          return;
        }
        await new Promise((r) => setTimeout(r, 3000));
      }
    }
    poll();
    return () => {
      stop = true;
    };
  }, [id]);

  const tier = ev?.tier ? TIER_COPY[ev.tier] || [ev.tier.toUpperCase(), "#16211e"] : null;

  return (
    <main className="max-w-3xl mx-auto px-6 py-12">
      <a href="/" className="docket-line text-[--docket]">← OpenNIW</a>
      <div className="mt-8 border border-[--rule] bg-white">
        <div className="rule-b px-6 py-4 flex items-center justify-between flex-wrap gap-2">
          <span className="docket-line">Free Evaluation — Report</span>
          {tier && (
            <span className="docket-line px-2 py-1 border" style={{ color: tier[1], borderColor: tier[1] }}>
              {tier[0]}
            </span>
          )}
        </div>
        <div className="px-6 py-6">
          {error && <p className="text-[--stamp] text-sm">{error}</p>}
          {!error && (!ev || ev.status !== "done") && (
            <div className="py-16 text-center">
              <p className="drafting-caret text-lg" style={{ fontFamily: "var(--font-serif), serif" }}>
                Reading your record
              </p>
              <p className="docket-line mt-3 text-[#6b7570]">
                Fetching sources · consolidating profile · applying the Dhanasar framework
              </p>
            </div>
          )}
          {ev?.status === "done" && <Md>{ev.report_md}</Md>}
        </div>
      </div>
      {ev?.status === "done" && (
        <div className="mt-8 border border-[--docket] bg-[--field] px-6 py-6">
          <div className="docket-line text-[--docket] mb-2">Next — Stage II</div>
          <p className="text-sm mb-4">
            Turn this evaluation into a case: OpenNIW seeds your evidence
            checklist from this report and starts collecting automatically.
          </p>
          <a
            className="btn"
            href={getToken() ? `/dashboard?eval=${id}` : `/login?eval=${id}`}
          >
            Start my case
          </a>
        </div>
      )}
    </main>
  );
}
