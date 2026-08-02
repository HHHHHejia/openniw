"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { api } from "@/lib/api";
import { Header, FinishBar } from "@/components/session";

// Two percentile-band small multiples over the approved-case database —
// one per metric (citations / papers), sharing the same filters and
// x-axis: x = approval month, bands = P10–P90 / P25–P75, line = median;
// the user's own value is a dashed labeled reference line.
// Survivor-only data: copy speaks in percentiles-among-approved, never
// probability.

type Data = {
  generated: string; source: string; ym0: string;
  categories: string[]; fields: string[];
  cases: [number, number, number, number, number][];
};
type MonthRow = { ym: number; n: number; p: number[] };

const GREEN = "#1f6f54";
const STAMP = "#b3402a";
const MUTED = "#4f5a55";
const RULE = "#d8d5cc";

const W = 720, H = 240, PAD = { l: 54, r: 92, t: 12, b: 24 };

function pct(sorted: number[], p: number): number {
  if (!sorted.length) return 0;
  const i = (sorted.length - 1) * p;
  const lo = Math.floor(i), hi = Math.ceil(i);
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (i - lo);
}

const ylog = (c: number) => Math.log10(c + 1);

function fmt(n: number): string {
  return n >= 10000 ? `${Math.round(n / 1000)}k` : Math.round(n).toLocaleString();
}

function BandChart({ title, note, series, user, userLabel, ymLabel, ticks }: {
  title: string; note: string; series: MonthRow[];
  user: number | null; userLabel: string;
  ymLabel: (ym: number) => string; ticks: number[];
}) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [hoverX, setHoverX] = useState<number | null>(null);

  const scale = useMemo(() => {
    if (!series.length) return null;
    const x0 = series[0].ym, x1 = series[series.length - 1].ym;
    const yMax = Math.max(...series.map((s) => s.p[4]), user ?? 0) * 1.15 + 5;
    const X = (ym: number) =>
      PAD.l + ((ym - x0) / Math.max(1, x1 - x0)) * (W - PAD.l - PAD.r);
    const Y = (c: number) =>
      PAD.t + (1 - ylog(c) / ylog(yMax)) * (H - PAD.t - PAD.b);
    return { x0, x1, yMax, X, Y };
  }, [series, user]);

  if (!scale || series.length === 0) {
    return (
      <div className="border border-[--rule] bg-white px-4 py-6 text-center">
        <div className="docket-line mb-1">{title}</div>
        <p className="docket-line text-[#4f5a55]">
          Not enough approved cases for this filter.
        </p>
      </div>
    );
  }

  const hovered = hoverX != null
    ? series.reduce((best, s) =>
        Math.abs(scale.X(s.ym) - hoverX) < Math.abs(scale.X(best.ym) - hoverX)
          ? s : best, series[0])
    : null;

  const shownTicks = ticks.filter((t) => t < scale.yMax);
  const areaPath = (loIdx: number, hiIdx: number) => {
    const up = series.map((s) => `${scale.X(s.ym)},${scale.Y(s.p[hiIdx])}`);
    const dn = [...series].reverse()
      .map((s) => `${scale.X(s.ym)},${scale.Y(s.p[loIdx])}`);
    return `M${up.join("L")}L${dn.join("L")}Z`;
  };

  return (
    <div className="border border-[--rule] bg-white px-4 py-4 overflow-x-auto">
      <div className="docket-line mb-1">
        {title} <span className="text-[#4f5a55]">· {note}</span>
      </div>
      <svg ref={svgRef} viewBox={`0 0 ${W} ${H}`} className="w-full"
           onMouseMove={(e) => {
             const r = svgRef.current!.getBoundingClientRect();
             setHoverX((e.clientX - r.left) * (W / r.width));
           }}
           onMouseLeave={() => setHoverX(null)}>
        {shownTicks.map((t) => (
          <g key={t}>
            <line x1={PAD.l} x2={W - PAD.r} y1={scale.Y(t)} y2={scale.Y(t)}
                  stroke={RULE} strokeWidth={1} />
            <text x={PAD.l - 6} y={scale.Y(t) + 4} textAnchor="end"
                  fontSize={11} fill={MUTED}>{fmt(t)}</text>
          </g>
        ))}
        <path d={areaPath(0, 4)} fill={GREEN} opacity={0.13} />
        <path d={areaPath(1, 3)} fill={GREEN} opacity={0.25} />
        <path d={`M${series.map((s) => `${scale.X(s.ym)},${scale.Y(s.p[2])}`).join("L")}`}
              fill="none" stroke={GREEN} strokeWidth={2} />
        <text x={W - PAD.r + 6} y={scale.Y(series[series.length - 1].p[2]) + 4}
              fontSize={11} fill={GREEN}>median</text>
        {user != null && (
          <g>
            <line x1={PAD.l} x2={W - PAD.r} y1={scale.Y(user)} y2={scale.Y(user)}
                  stroke={STAMP} strokeWidth={2} strokeDasharray="7 4" />
            <text x={W - PAD.r + 6} y={scale.Y(user) + 4} fontSize={11}
                  fill={STAMP} fontWeight={600}>
              {userLabel} · {fmt(user)}
            </text>
          </g>
        )}
        {series.filter((_, i) => i % Math.ceil(series.length / 7) === 0)
          .map((s) => (
            <text key={s.ym} x={scale.X(s.ym)} y={H - 6} textAnchor="middle"
                  fontSize={11} fill={MUTED}>{ymLabel(s.ym)}</text>
          ))}
        {hovered && (
          <g>
            <line x1={scale.X(hovered.ym)} x2={scale.X(hovered.ym)}
                  y1={PAD.t} y2={H - PAD.b} stroke={MUTED} strokeWidth={1}
                  strokeDasharray="2 3" />
            {(() => {
              const tx = Math.min(scale.X(hovered.ym) + 10, W - 195);
              return (
                <g transform={`translate(${tx},${PAD.t + 2})`}>
                  <rect width={180} height={96} fill="#fff" stroke={RULE} />
                  <text x={8} y={16} fontSize={11} fontWeight={600} fill="#16211e">
                    {ymLabel(hovered.ym)} · {hovered.n} approved
                  </text>
                  {[["P90", hovered.p[4]], ["P75", hovered.p[3]],
                    ["median", hovered.p[2]], ["P25", hovered.p[1]],
                    ["P10", hovered.p[0]]].map(([lab, v], i) => (
                    <text key={String(lab)} x={8} y={32 + i * 13} fontSize={11} fill={MUTED}>
                      {lab}: {fmt(v as number)}
                    </text>
                  ))}
                </g>
              );
            })()}
          </g>
        )}
      </svg>
    </div>
  );
}

export default function BenchmarkPage() {
  const [data, setData] = useState<Data | null>(null);
  const [category, setCategory] = useState("NIW");
  const [field, setField] = useState<string>("All fields");
  const [cites, setCites] = useState<string>("");
  const [pubs, setPubs] = useState<string>("");
  const [range, setRange] = useState<"recent" | "5y" | "all">("recent");
  const [view, setView] = useState<"chart" | "table">("chart");
  const [saved, setSaved] = useState(false);
  const [savedOnce, setSavedOnce] = useState(false);

  useEffect(() => {
    fetch("/benchmark-data.json").then((r) => r.json()).then(setData)
      .catch(() => {});
    api("/api/benchmark/inputs").then((r) => {
      const s = r.inputs || {};
      if (s.category) setCategory(s.category);
      if (s.field) setField(s.field);
      if (s.citations != null) setCites(String(s.citations));
      if (s.publications != null) setPubs(String(s.publications));
      if (Object.keys(s).length) setSavedOnce(true);
    }).catch(() => {});
  }, []);

  const ym0 = useMemo(() => {
    if (!data) return [2012, 1];
    const [y, m] = data.ym0.split("-").map(Number);
    return [y, m];
  }, [data]);
  const ymLabel = (ym: number) => {
    const y = ym0[0] + Math.floor((ym + ym0[1] - 1) / 12);
    const m = ((ym + ym0[1] - 1) % 12) + 1;
    return `${y}-${String(m).padStart(2, "0")}`;
  };

  const myCites = cites === "" ? null : Math.max(0, Number(cites) || 0);
  const myPubs = pubs === "" ? null : Math.max(0, Number(pubs) || 0);

  const filtered = useMemo(() => {
    if (!data) return [];
    const ci = data.categories.indexOf(category);
    const fi = field === "All fields" ? -1 : data.fields.indexOf(field);
    const maxYm = Math.max(...data.cases.map((c) => c[0]));
    const minYm = range === "all" ? 0
      : range === "5y" ? maxYm - 59 : maxYm - 41;
    return data.cases.filter((c) =>
      c[1] === ci && (fi === -1 || c[2] === fi) && c[0] >= minYm);
  }, [data, category, field, range]);

  const recent24 = useMemo(() => {
    if (!filtered.length) return [];
    const maxYm = Math.max(...filtered.map((c) => c[0]));
    return filtered.filter((c) => c[0] >= maxYm - 23);
  }, [filtered]);

  const stats = useMemo(() => {
    const pool = recent24.length >= 30 ? recent24 : filtered;
    const cs = pool.map((c) => c[3]).sort((a, b) => a - b);
    const ps = pool.map((c) => c[4]).filter((p) => p >= 0).sort((a, b) => a - b);
    const pctOf = (sorted: number[], v: number | null) =>
      v == null || !sorted.length ? null
        : Math.round(100 * sorted.filter((x) => x <= v).length / sorted.length);
    return {
      n: pool.length, poolIsRecent: recent24.length >= 30,
      medianCites: pct(cs, 0.5), medianPubs: ps.length ? pct(ps, 0.5) : null,
      citesPercentile: pctOf(cs, myCites),
      pubsPercentile: pctOf(ps, myPubs),
      lowWins: myCites == null ? null
        : recent24.filter((c) => c[3] <= myCites).length,
    };
  }, [filtered, recent24, myCites, myPubs]);

  const makeSeries = (metricIdx: 3 | 4): MonthRow[] => {
    const byYm = new Map<number, number[]>();
    filtered.forEach((c) => {
      const v = c[metricIdx];
      if (v < 0) return;
      if (!byYm.has(c[0])) byYm.set(c[0], []);
      byYm.get(c[0])!.push(v);
    });
    const yms = Array.from(byYm.keys()).sort((a, b) => a - b);
    const out: MonthRow[] = [];
    for (const ym of yms) {
      const win = [byYm.get(ym - 1) || [], byYm.get(ym) || [],
                   byYm.get(ym + 1) || []].flat().sort((a, b) => a - b);
      if (win.length < 5) continue;
      out.push({ ym, n: (byYm.get(ym) || []).length,
                 p: [0.1, 0.25, 0.5, 0.75, 0.9].map((q) => pct(win, q)) });
    }
    return out;
  };
  const citesSeries = useMemo(() => makeSeries(3), [filtered]);
  const pubsSeries = useMemo(() => makeSeries(4), [filtered]);

  async function save() {
    await api("/api/benchmark/inputs", {
      method: "PUT",
      body: { inputs: {
        category, field, citations: myCites, publications: myPubs,
        computed: {
          citations_percentile_among_approved: stats.citesPercentile,
          publications_percentile_among_approved: stats.pubsPercentile,
          window: stats.poolIsRecent ? "last 24 months" : "selected range",
          sample_n: stats.n,
          peer_median_citations: Math.round(stats.medianCites),
          peer_median_publications:
            stats.medianPubs == null ? null : Math.round(stats.medianPubs),
          low_citation_precedents_24mo: stats.lowWins,
        },
      } },
    });
    setSaved(true);
    setSavedOnce(true);
    setTimeout(() => setSaved(false), 1800);
  }

  if (!data) return <p className="docket-line p-8">Loading approved-case data…</p>;

  const tile = (label: string, value: string, sub?: string, accent?: boolean) => (
    <div className={`border ${accent ? "border-[--docket]" : "border-[--rule]"} bg-white px-4 py-3`}>
      <div className="docket-line text-[#4f5a55]">{label}</div>
      <div className="text-3xl" style={{ fontFamily: "var(--font-serif), serif",
                                         color: accent ? GREEN : undefined }}>
        {value}
      </div>
      {sub && <div className="text-xs text-[#4f5a55]">{sub}</div>}
    </div>
  );
  const poolNote = `of approved ${field === "All fields" ? "" : "same-field "}peers (${stats.poolIsRecent ? "last 24 mo" : "selected range"})`;

  const bmSteps = (myCites != null || myPubs != null ? 1 : 0) + (savedOnce ? 1 : 0);
  return (
    <div className="max-w-4xl mx-auto px-6 py-6">
      <Header active="benchmark"
              progress={{
                label: savedOnce ? "saved to your case ✓"
                  : (myCites != null || myPubs != null)
                    ? "now: Save to my case" : "enter your numbers below",
                done: bmSteps, total: 2,
              }} />
      <h1 className="text-2xl mb-1" style={{ fontFamily: "var(--font-serif), serif" }}>
        How you compare with approved cases
      </h1>
      <p className="text-sm text-[#4f5a55] mb-1 leading-relaxed">
        7,458 publicly posted I-140 approvals, 2012–2026. Enter your numbers
        to see where you sit among approved peers in your field.
      </p>
      <p className="docket-line text-[--stamp] mb-5">
        Approved cases only — this shows what approved profiles look like,
        NOT your approval probability.
      </p>

      <div className="flex flex-wrap gap-3 items-end mb-5">
        <label className="text-xs">
          <span className="docket-line block mb-0.5">Category</span>
          <select value={category} onChange={(e) => setCategory(e.target.value)}>
            {data.categories.filter((c) => ["NIW", "EB1A", "EB1B"].includes(c))
              .map((c) => <option key={c}>{c}</option>)}
          </select>
        </label>
        <label className="text-xs">
          <span className="docket-line block mb-0.5">Your field</span>
          <select value={field} onChange={(e) => setField(e.target.value)}>
            <option>All fields</option>
            {data.fields.map((f) => <option key={f}>{f}</option>)}
          </select>
        </label>
        <label className="text-xs">
          <span className="docket-line block mb-0.5">Your citations</span>
          <input type="number" min={0} className="!w-28" value={cites}
                 placeholder="e.g. 350"
                 onChange={(e) => setCites(e.target.value)} />
        </label>
        <label className="text-xs">
          <span className="docket-line block mb-0.5">Your papers</span>
          <input type="number" min={0} className="!w-24" value={pubs}
                 placeholder="e.g. 15"
                 onChange={(e) => setPubs(e.target.value)} />
        </label>
        <label className="text-xs">
          <span className="docket-line block mb-0.5">Period</span>
          <select value={range} onChange={(e) => setRange(e.target.value as any)}>
            <option value="recent">2023 – now</option>
            <option value="5y">Last 5 years</option>
            <option value="all">All years</option>
          </select>
        </label>
        <button className="btn-quiet !py-1.5 docket-line ml-auto"
                onClick={() => setView(view === "chart" ? "table" : "chart")}>
          {view === "chart" ? "table view" : "chart view"}
        </button>
      </div>

      <div className="grid sm:grid-cols-4 gap-3 mb-5">
        {tile("Citations percentile",
              stats.citesPercentile == null ? "—" : `${stats.citesPercentile}%`,
              stats.citesPercentile == null ? "enter your citations"
                : `${poolNote} have ≤ your citations`, true)}
        {tile("Papers percentile",
              stats.pubsPercentile == null ? "—" : `${stats.pubsPercentile}%`,
              stats.pubsPercentile == null ? "enter your paper count"
                : `${poolNote} have ≤ your papers`, true)}
        {tile("Peer medians",
              `${fmt(stats.medianCites)} · ${stats.medianPubs == null ? "—" : Math.round(stats.medianPubs)}`,
              "citations · papers")}
        {tile("Approved sample", stats.n.toLocaleString(),
              stats.n < 30 ? "small sample — interpret loosely" : undefined)}
      </div>

      {myCites != null && stats.lowWins != null && stats.lowWins > 0 &&
        stats.citesPercentile != null && stats.citesPercentile < 40 && (
        <p className="text-sm text-[#4f5a55] mb-4">
          Encouragement: <b>{stats.lowWins}</b> approved {category} case{stats.lowWins > 1 ? "s" : ""} in
          the last 24 months had citations at or below yours — citations are
          one factor, not a threshold.
        </p>
      )}

      {view === "chart" ? (
        <div className="grid gap-4">
          <BandChart
            title="Citations of approved cases by month"
            note="bands: middle 50% and 80% · 3-month window · log scale"
            series={citesSeries} user={myCites} userLabel="You"
            ymLabel={ymLabel} ticks={[10, 100, 1000, 10000, 50000]} />
          <BandChart
            title="Papers of approved cases by month"
            note="journal + conference papers · same window · log scale"
            series={pubsSeries} user={myPubs} userLabel="You"
            ymLabel={ymLabel} ticks={[5, 10, 25, 50, 100, 250]} />
        </div>
      ) : (
        <div className="border border-[--rule] bg-white px-4 py-4 overflow-x-auto">
          <table className="text-sm w-full">
            <thead>
              <tr className="docket-line text-left">
                <th className="pr-3 pb-2">Month</th><th className="pr-3 pb-2">n</th>
                <th className="pr-3 pb-2">Cites P25</th>
                <th className="pr-3 pb-2">Cites med</th>
                <th className="pr-3 pb-2">Cites P75</th>
                <th className="pr-3 pb-2">Papers P25</th>
                <th className="pr-3 pb-2">Papers med</th>
                <th className="pr-3 pb-2">Papers P75</th>
              </tr>
            </thead>
            <tbody>
              {[...citesSeries].reverse().map((s) => {
                const ps = pubsSeries.find((x) => x.ym === s.ym);
                return (
                  <tr key={s.ym} className="border-t border-[--rule]">
                    <td className="pr-3 py-1">{ymLabel(s.ym)}</td>
                    <td className="pr-3">{s.n}</td>
                    <td className="pr-3">{fmt(s.p[1])}</td>
                    <td className="pr-3">{fmt(s.p[2])}</td>
                    <td className="pr-3">{fmt(s.p[3])}</td>
                    <td className="pr-3">{ps ? fmt(ps.p[1]) : "—"}</td>
                    <td className="pr-3">{ps ? fmt(ps.p[2]) : "—"}</td>
                    <td className="pr-3">{ps ? fmt(ps.p[3]) : "—"}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      <div className="flex items-center justify-between mt-5">
        <p className="text-xs text-[#4f5a55] max-w-md leading-relaxed">
          {data.source} Generated {data.generated}. Figures self-reported by
          the law firm, not verified by USCIS.
        </p>
        <button className="btn" onClick={save}
                disabled={myCites == null && myPubs == null}>
          {saved ? "Saved to case ✓" : "Save to my case"}
        </button>
      </div>

      <FinishBar
        beforeFinish={async () => { if (myCites != null || myPubs != null) await save(); }}
        summary={() => ({
          benchmark: {
            category, field, citations: myCites, publications: myPubs,
            citations_percentile: stats.citesPercentile,
            publications_percentile: stats.pubsPercentile,
          },
        })}
      />
    </div>
  );
}
