"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { SiteNav, SiteFooter } from "@/components/nav";

// The evaluation bench, built on 10,999 publicly posted approvals.
// Sections (per the DB design doc's priorities): peer histogram + what-if
// slider · NIW-vs-EB1A dual track · processing-time simulation · monthly
// trend bands · action-insight cards · weekly pulse. Copy rules: numbers
// are always distributions of APPROVED cases, never probabilities; small
// samples widen automatically and say so; default window is 2024+.

type Data = {
  generated: string; source: string; ym0: string;
  categories: string[]; fields: string[];
  premium_codes: Record<string, string>;
  aggregates: {
    rec_letters_niw_hist: Record<string, number>;
    rfe_overcome_2024: { rate: number; n: number };
    weekly: [string, number, number, number][];
  };
  cases: [number, number, number, number, number, number, number][];
};
type MonthRow = { ym: number; n: number; p: number[] };

const GREEN = "#1f6f54";
const STAMP = "#b3402a";
const MUTED = "#4f5a55";
const RULE = "#d8d5cc";
const FIELDBG = "#f0eee6";

const W = 720, H = 240, PAD = { l: 54, r: 92, t: 12, b: 24 };

function pct(sorted: number[], p: number): number {
  if (!sorted.length) return 0;
  const i = (sorted.length - 1) * p;
  const lo = Math.floor(i), hi = Math.ceil(i);
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (i - lo);
}
function fmt(n: number): string {
  return n >= 10000 ? `${Math.round(n / 1000)}k` : Math.round(n).toLocaleString();
}

function niceStep(raw: number): number {
  if (raw <= 0) return 1;
  let unit = 1, scaled = raw;
  while (scaled >= 10) { scaled /= 10; unit *= 10; }
  while (scaled < 1) { scaled *= 10; unit /= 10; }
  const nice = scaled <= 1 ? 1 : scaled <= 2 ? 2 : scaled <= 5 ? 5 : 10;
  return Math.max(1, nice * unit);
}

const CITE_BUCKETS: [string, number, number][] = [
  ["0–49", 0, 50], ["50–99", 50, 100], ["100–199", 100, 200],
  ["200–499", 200, 500], ["500+", 500, Infinity],
];

// ---------------------------------------------------------------- charts --
function BandChart({ title, note, series, user, ymLabel }: {
  title: string; note: string; series: MonthRow[];
  user: number | null; ymLabel: (ym: number) => string;
}) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [hoverX, setHoverX] = useState<number | null>(null);
  const scale = useMemo(() => {
    if (!series.length) return null;
    const x0 = series[0].ym, x1 = series[series.length - 1].ym;
    const rawMax = Math.max(1, ...series.map((s) => s.p[4]), user ?? 0) * 1.1;
    const step = niceStep(rawMax / 4);
    const yMax = Math.ceil(rawMax / step) * step;
    const ticks = Array.from(
      { length: Math.floor(yMax / step) + 1 }, (_, i) => i * step,
    );
    return {
      x0, x1, yMax, ticks,
      X: (ym: number) => PAD.l + ((ym - x0) / Math.max(1, x1 - x0)) * (W - PAD.l - PAD.r),
      Y: (c: number) => PAD.t + (1 - c / yMax) * (H - PAD.t - PAD.b),
    };
  }, [series, user]);
  if (!scale) return null;
  const hovered = hoverX != null
    ? series.reduce((b, s) => Math.abs(scale.X(s.ym) - hoverX) < Math.abs(scale.X(b.ym) - hoverX) ? s : b, series[0])
    : null;
  const area = (lo: number, hi: number) =>
    `M${series.map((s) => `${scale.X(s.ym)},${scale.Y(s.p[hi])}`).join("L")}L${[...series].reverse().map((s) => `${scale.X(s.ym)},${scale.Y(s.p[lo])}`).join("L")}Z`;
  return (
    <div className="border border-[--rule] bg-white px-4 py-4 overflow-x-auto">
      <div className="docket-line mb-1">{title} <span className="text-[#4f5a55]">· {note}</span></div>
      <svg ref={svgRef} viewBox={`0 0 ${W} ${H}`} className="w-full"
           onMouseMove={(e) => {
             const r = svgRef.current!.getBoundingClientRect();
             setHoverX((e.clientX - r.left) * (W / r.width));
           }}
           onMouseLeave={() => setHoverX(null)}>
        {scale.ticks.map((t) => (
          <g key={t}>
            <line x1={PAD.l} x2={W - PAD.r} y1={scale.Y(t)} y2={scale.Y(t)} stroke={RULE} />
            <text x={PAD.l - 6} y={scale.Y(t) + 4} textAnchor="end" fontSize={11} fill={MUTED}>{fmt(t)}</text>
          </g>
        ))}
        <path d={area(0, 4)} fill={GREEN} opacity={0.13} />
        <path d={area(1, 3)} fill={GREEN} opacity={0.25} />
        <path d={`M${series.map((s) => `${scale.X(s.ym)},${scale.Y(s.p[2])}`).join("L")}`}
              fill="none" stroke={GREEN} strokeWidth={2} />
        <text x={W - PAD.r + 6} y={scale.Y(series[series.length - 1].p[2]) + 4} fontSize={11} fill={GREEN}>median</text>
        {user != null && (
          <g>
            <line x1={PAD.l} x2={W - PAD.r} y1={scale.Y(user)} y2={scale.Y(user)}
                  stroke={STAMP} strokeWidth={2} strokeDasharray="7 4" />
            <text x={W - PAD.r + 6} y={scale.Y(user) + 4} fontSize={11} fill={STAMP} fontWeight={600}>
              You · {fmt(user)}
            </text>
          </g>
        )}
        {series.filter((_, i) => i % Math.ceil(series.length / 7) === 0).map((s) => (
          <text key={s.ym} x={scale.X(s.ym)} y={H - 6} textAnchor="middle" fontSize={11} fill={MUTED}>
            {ymLabel(s.ym)}
          </text>
        ))}
        {hovered && (
          <g>
            <line x1={scale.X(hovered.ym)} x2={scale.X(hovered.ym)} y1={PAD.t} y2={H - PAD.b}
                  stroke={MUTED} strokeDasharray="2 3" />
            <g transform={`translate(${Math.min(scale.X(hovered.ym) + 10, W - 195)},${PAD.t + 2})`}>
              <rect width={180} height={96} fill="#fff" stroke={RULE} />
              <text x={8} y={16} fontSize={11} fontWeight={600} fill="#16211e">
                {ymLabel(hovered.ym)} · {hovered.n} approved
              </text>
              {[["P90", hovered.p[4]], ["P75", hovered.p[3]], ["median", hovered.p[2]],
                ["P25", hovered.p[1]], ["P10", hovered.p[0]]].map(([lab, v], i) => (
                <text key={String(lab)} x={8} y={32 + i * 13} fontSize={11} fill={MUTED}>
                  {lab}: {fmt(v as number)}
                </text>
              ))}
            </g>
          </g>
        )}
      </svg>
    </div>
  );
}

// ------------------------------------------------------------------ page --
export default function BenchmarkPage() {
  const [data, setData] = useState<Data | null>(null);
  const [category, setCategory] = useState("NIW");
  const [field, setField] = useState<string>("All fields");
  const [cites, setCites] = useState<string>("");
  const [pubs, setPubs] = useState<string>("");
  const [range, setRange] = useState<"recent" | "5y" | "all">("recent");
  const [premiumPlan, setPremiumPlan] = useState<"1" | "2" | "0">("1");

  useEffect(() => {
    fetch("/benchmark-data.json").then((r) => r.json()).then(setData).catch(() => {});
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
  const ymOf = (y: number, m: number) => (y - ym0[0]) * 12 + (m - ym0[1]);

  const myCites = cites === "" ? null : Math.max(0, Number(cites) || 0);
  const myPubs = pubs === "" ? null : Math.max(0, Number(pubs) || 0);

  const inRange = (c: Data["cases"][0]) => {
    if (!data) return false;
    if (range === "all") return true;
    if (range === "recent") return c[0] >= ymOf(2024, 1);
    const maxYm = data.cases[data.cases.length - 1][0];
    return c[0] >= maxYm - 59;
  };

  // pool for a category with the doc's widening rule: field n<30 → all fields
  const poolFor = (cat: string) => {
    if (!data) return { rows: [] as Data["cases"], widened: false };
    const ci = data.categories.indexOf(cat);
    const fi = field === "All fields" ? -1 : data.fields.indexOf(field);
    const base = data.cases.filter((c) => c[1] === ci && inRange(c));
    const fielded = fi === -1 ? base : base.filter((c) => c[2] === fi);
    if (fielded.length >= 30 || fi === -1)
      return { rows: fielded, widened: false };
    return { rows: base, widened: true };
  };

  const pool = useMemo(() => poolFor(category), [data, category, field, range]);
  const filtered = pool.rows;

  const stats = useMemo(() => {
    const cs = filtered.map((c) => c[3]).sort((a, b) => a - b);
    const ps = filtered.map((c) => c[4]).filter((p) => p >= 0).sort((a, b) => a - b);
    const pctOf = (sorted: number[], v: number | null) =>
      v == null || !sorted.length ? null
        : Math.round(100 * sorted.filter((x) => x <= v).length / sorted.length);
    return {
      n: filtered.length,
      medianCites: pct(cs, 0.5), medianPubs: ps.length ? pct(ps, 0.5) : null,
      citesPercentile: pctOf(cs, myCites), pubsPercentile: pctOf(ps, myPubs),
      lowWins: myCites == null ? null : filtered.filter((c) => c[3] <= myCites).length,
      cs,
    };
  }, [filtered, myCites, myPubs]);

  const histo = useMemo(() => {
    const total = filtered.length || 1;
    return CITE_BUCKETS.map(([label, lo, hi]) => ({
      label, lo, hi,
      n: filtered.filter((c) => c[3] >= lo && c[3] < hi).length,
      share: filtered.filter((c) => c[3] >= lo && c[3] < hi).length / total,
    }));
  }, [filtered]);

  const dual = useMemo(() => {
    if (!data || myCites == null) return null;
    return ["NIW", "EB1A"].map((cat) => {
      const p = poolFor(cat);
      const cs = p.rows.map((c) => c[3]).sort((a, b) => a - b);
      return {
        cat, n: cs.length,
        pct: cs.length ? Math.round(100 * cs.filter((x) => x <= myCites).length / cs.length) : null,
      };
    });
  }, [data, myCites, field, range]);

  const timeline = useMemo(() => {
    if (!data) return null;
    const ci = data.categories.indexOf(category);
    const days = data.cases
      .filter((c) => c[1] === ci && inRange(c) && c[5] >= 0
        && String(c[6]) === premiumPlan)
      .map((c) => c[5]).sort((a, b) => a - b);
    if (days.length < 20) return { n: days.length, p: null as null | number[] };
    return { n: days.length, p: [0.25, 0.5, 0.75].map((q) => pct(days, q)) };
  }, [data, category, range, premiumPlan]);

  const makeSeries = (metricIdx: 3 | 4): MonthRow[] => {
    const byYm = new Map<number, number[]>();
    filtered.forEach((c) => {
      const v = c[metricIdx];
      if (v < 0) return;
      if (!byYm.has(c[0])) byYm.set(c[0], []);
      byYm.get(c[0])!.push(v);
    });
    const out: MonthRow[] = [];
    for (const ym of Array.from(byYm.keys()).sort((a, b) => a - b)) {
      const win = [byYm.get(ym - 1) || [], byYm.get(ym) || [], byYm.get(ym + 1) || []]
        .flat().sort((a, b) => a - b);
      if (win.length < 5) continue;
      out.push({ ym, n: (byYm.get(ym) || []).length,
                 p: [0.1, 0.25, 0.5, 0.75, 0.9].map((q) => pct(win, q)) });
    }
    return out;
  };
  const citesSeries = useMemo(() => makeSeries(3), [filtered]);
  const pubsSeries = useMemo(() => makeSeries(4), [filtered]);

  if (!data) return <p className="docket-line p-8">Loading approved-case data…</p>;

  const poolNote =
    `${pool.widened ? "all fields (your field's sample was small)" : field === "All fields" ? "all fields" : "your field"}, ${range === "recent" ? "2024+" : range === "5y" ? "last 5 years" : "all years"}`;
  const today = new Date();
  const plusDays = (d: number) => {
    const dt = new Date(today.getTime() + d * 86400000);
    return dt.toLocaleDateString("en-US", { month: "short", year: "numeric" });
  };
  const tile = (label: string, value: string, sub?: string, accent?: boolean) => (
    <div className={`border ${accent ? "border-[--docket]" : "border-[--rule]"} bg-white px-4 py-3`}>
      <div className="docket-line text-[#4f5a55]">{label}</div>
      <div className="text-3xl" style={{ fontFamily: "var(--font-serif), serif", color: accent ? GREEN : undefined }}>
        {value}
      </div>
      {sub && <div className="text-xs text-[#4f5a55]">{sub}</div>}
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto px-6 py-6">
      <SiteNav active="eval" />
      <h1 className="text-2xl mb-1" style={{ fontFamily: "var(--font-serif), serif" }}>
        How you compare with approved cases
      </h1>
      <p className="docket-line text-[--stamp] mb-5">
        Approved cases only — this shows what approved profiles look like,
        NOT your approval probability.
      </p>

      {/* controls */}
      <div className="flex flex-wrap gap-3 items-end mb-5">
        <label className="text-xs">
          <span className="docket-line block mb-0.5">Category</span>
          <select value={category} onChange={(e) => setCategory(e.target.value)}>
            {data.categories.filter((c) => ["NIW", "EB1A", "EB1B", "O1"].includes(c)).map((c) => <option key={c}>{c}</option>)}
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
                 placeholder="e.g. 350" onChange={(e) => setCites(e.target.value)} />
        </label>
        <label className="text-xs">
          <span className="docket-line block mb-0.5">Your papers</span>
          <input type="number" min={0} className="!w-24" value={pubs}
                 placeholder="e.g. 15" onChange={(e) => setPubs(e.target.value)} />
        </label>
        <label className="text-xs">
          <span className="docket-line block mb-0.5">Period</span>
          <select value={range} onChange={(e) => setRange(e.target.value as any)}>
            <option value="recent">2024 – now (default)</option>
            <option value="5y">Last 5 years</option>
            <option value="all">All years</option>
          </select>
        </label>
      </div>

      {/* tiles */}
      <div className="grid sm:grid-cols-4 gap-3 mb-2">
        {tile("Citations percentile",
              stats.citesPercentile == null ? "—" : `${stats.citesPercentile}%`,
              stats.citesPercentile == null ? "enter your citations"
                : `of approved peers (${poolNote}) have ≤ yours`, true)}
        {tile("Papers percentile",
              stats.pubsPercentile == null ? "—" : `${stats.pubsPercentile}%`,
              stats.pubsPercentile == null ? "enter your paper count"
                : "same pool, papers", true)}
        {tile("Peer medians",
              `${fmt(stats.medianCites)} · ${stats.medianPubs == null ? "—" : Math.round(stats.medianPubs)}`,
              "citations · papers")}
        {tile("Approved sample", stats.n.toLocaleString(),
              pool.widened ? "widened to all fields" : stats.n < 30 ? "small — interpret loosely" : undefined)}
      </div>
      {stats.n > 0 && stats.n < 200 && (
        <p className="text-sm border border-[--docket] bg-[--field] px-4 py-2.5 mb-3">
          <b>Small pool.</b> Only {stats.n.toLocaleString()} publicly posted
          approved {category} cases match this window — read every band and
          percentile as a rough anchor among approved cases, never a precise
          cutoff (and never an approval probability).
        </p>
      )}
      {myCites != null && stats.lowWins != null && stats.lowWins > 0 &&
        stats.citesPercentile != null && stats.citesPercentile < 40 && (
        <p className="text-sm text-[#4f5a55] mb-2">
          <b>{stats.lowWins}</b> approved {category} cases in this pool had
          citations at or below yours — approved profiles vary widely on this dimension.
        </p>
      )}

      {/* trend bands — the highest-information view, so they lead */}
      <div className="grid gap-4 mt-3 mb-4">
        <BandChart title="Citations of approved cases by month"
                   note="bands: middle 50% and 80% · 3-month window · linear scale"
                   series={citesSeries} user={myCites} ymLabel={ymLabel} />
        <BandChart title="Papers of approved cases by month"
                   note="journal + conference papers · same window · linear scale"
                   series={pubsSeries} user={myPubs} ymLabel={ymLabel} />
      </div>

      {/* histogram + what-if slider */}
      <section className="border border-[--rule] bg-white px-5 py-4 mb-4">
        <div className="docket-line mb-3">
          Where approved cases sit by citations
          <span className="text-[#4f5a55]"> · {poolNote} · n={stats.n}</span>
        </div>
        <div className="flex items-end gap-2 h-36">
          {histo.map((b) => {
            const isYou = myCites != null && myCites >= b.lo && myCites < b.hi;
            const max = Math.max(...histo.map((x) => x.share), 0.01);
            return (
              <div key={b.label} className="flex-1 flex flex-col items-center justify-end h-full">
                <span className="docket-line !text-[0.7rem] mb-1">{b.n}</span>
                <div className="w-full relative"
                     style={{ height: `${Math.max(3, 100 * b.share / max)}%`,
                              background: GREEN, opacity: isYou ? 1 : 0.45,
                              outline: isYou ? `2px solid ${STAMP}` : "none",
                              outlineOffset: 2 }} />
                <span className={`docket-line !text-[0.7rem] mt-1.5 ${isYou ? "font-bold" : "text-[#4f5a55]"}`}>
                  {b.label}{isYou ? " ← you" : ""}
                </span>
              </div>
            );
          })}
        </div>
        <div className="mt-4 border-t border-[--rule] pt-3">
          <div className="docket-line text-[#4f5a55] mb-1">What-if: drag to explore</div>
          <input type="range" min={0} max={1500} step={10}
                 value={myCites ?? 0} className="w-full"
                 style={{ accentColor: GREEN }}
                 onChange={(e) => setCites(e.target.value)} />
          <p className="text-sm mt-1">
            {myCites == null ? "Drag the slider or type your citations above."
              : <>At <b>{fmt(myCites)}</b> citations you&apos;d be above{" "}
                 <b style={{ color: GREEN }}>{stats.citesPercentile}%</b> of
                 approved peers in this pool.</>}
          </p>
        </div>
      </section>

      {/* dual track */}
      {dual && (
        <section className="border border-[--rule] bg-white px-5 py-4 mb-4">
          <div className="docket-line mb-3">Same profile, two tracks</div>
          {dual.map((d) => (
            <div key={d.cat} className="mb-3">
              <div className="flex justify-between docket-line text-[#4f5a55] mb-1">
                <span>{d.cat}</span>
                <span>{d.pct == null ? "no sample" : `you're at P${d.pct} · n=${d.n.toLocaleString()}`}</span>
              </div>
              <div className="h-4 relative" style={{ background: FIELDBG, border: `1px solid ${RULE}` }}>
                {d.pct != null && (
                  <div className="absolute top-[-3px] h-[22px] w-[3px]"
                       style={{ left: `${d.pct}%`, background: STAMP }} />
                )}
              </div>
            </div>
          ))}
          <p className="text-xs text-[#4f5a55]">
            The same citation count usually sits at a much lower percentile
            among EB1A approvals — the two categories have very different
            approved-profile distributions. Scale: percentile among approved
            cases of that track (left = below most, right = above most).
          </p>
        </section>
      )}

      {/* processing-time simulation */}
      <section className="border border-[--rule] bg-white px-5 py-4 mb-4">
        <div className="docket-line mb-3">
          If you filed today — how long until approval?
          <span className="text-[#4f5a55]"> · approved {category} cases, {range === "recent" ? "2024+" : "selected period"}</span>
        </div>
        <div className="flex gap-2 mb-3">
          {[["1", "Premium"], ["2", "Mid-case upgrade"], ["0", "No / undisclosed premium"]].map(([code, label]) => (
            <button key={code} type="button"
                    className={`docket-line px-3 py-1.5 border ${premiumPlan === code ? "border-[--docket] text-[--docket]" : "border-[--rule]"}`}
                    onClick={() => setPremiumPlan(code as any)}>
              {label}
            </button>
          ))}
        </div>
        {timeline?.p ? (
          <div>
            <div className="relative h-8 mb-1" style={{ background: FIELDBG, border: `1px solid ${RULE}` }}>
              {(() => {
                const maxD = timeline.p![2] * 1.25;
                return (
                  <>
                    <div className="absolute h-full" style={{
                      left: `${100 * timeline.p![0] / maxD}%`,
                      width: `${100 * (timeline.p![2] - timeline.p![0]) / maxD}%`,
                      background: GREEN, opacity: 0.3 }} />
                    <div className="absolute h-full w-[3px]" style={{
                      left: `${100 * timeline.p![1] / maxD}%`, background: GREEN }} />
                  </>
                );
              })()}
            </div>
            <div className="flex justify-between text-xs text-[#4f5a55]">
              <span>fastest quarter: ≤{Math.round(timeline.p[0])} days ({plusDays(timeline.p[0])})</span>
              <span className="text-[--docket] font-semibold">median {Math.round(timeline.p[1])} days → {plusDays(timeline.p[1])}</span>
              <span>slowest quarter: ≥{Math.round(timeline.p[2])} days ({plusDays(timeline.p[2])})</span>
            </div>
            <p className="text-xs text-[#4f5a55] mt-2">
              Based on {timeline.n.toLocaleString()} approved cases that
              disclosed processing time. &quot;No premium&quot; includes cases that
              simply didn&apos;t mention it.
            </p>
          </div>
        ) : (
          <p className="docket-line text-[#4f5a55]">
            Too few disclosed timings for this combination (n={timeline?.n ?? 0}).
          </p>
        )}
      </section>

      {/* insight cards */}
      <div className="grid sm:grid-cols-2 gap-3 mb-4">
        <div className="border border-[--rule] bg-white px-4 py-3">
          <div className="docket-line text-[--docket] mb-1">Support letters</div>
          <p className="text-sm leading-relaxed">
            Approved NIW cases that disclosed a letter count usually filed{" "}
            <b>2–6 letters</b> (median 4). Planning for <b>~4</b> is the
            evidence-backed default.
          </p>
          <p className="text-xs text-[#4f5a55] mt-1">
            Based on {Object.values(data.aggregates.rec_letters_niw_hist).reduce((a, b) => a + b, 0).toLocaleString()} disclosing cases, all years.
          </p>
        </div>
        <div className="border border-[--rule] bg-white px-4 py-3">
          <div className="docket-line text-[--docket] mb-1">If an RFE comes</div>
          <p className="text-sm leading-relaxed">
            Among 2024+ approved NIW cases that disclosed their RFE status,{" "}
            <b>{data.aggregates.rfe_overcome_2024.rate}%</b> had received an
            RFE and later received approval.
          </p>
          <p className="text-xs text-[#4f5a55] mt-1">
            Based on {data.aggregates.rfe_overcome_2024.n} disclosing cases.
          </p>
        </div>
      </div>

      {/* weekly pulse */}
      {data.aggregates.weekly.length > 0 && (
        <section className="border border-[--rule] bg-white px-5 py-4 mb-4">
          <div className="docket-line mb-3">
            The latest pulse
            <span className="text-[#4f5a55]"> · weekly approvals at this firm · data through {data.aggregates.weekly[0][0]}</span>
          </div>
          <div className="flex items-end gap-1.5 h-20">
            {[...data.aggregates.weekly].reverse().map(([wk, total, niw]) => {
              const max = Math.max(...data.aggregates.weekly.map((w) => w[1]));
              return (
                <div key={wk} className="flex-1 flex flex-col items-center justify-end h-full"
                     title={`${wk}: ${total} approvals (${niw} NIW)`}>
                  <div className="w-full" style={{ height: `${100 * total / max}%`, background: GREEN, opacity: 0.5 }} />
                </div>
              );
            })}
          </div>
          <div className="flex justify-between docket-line !text-[0.7rem] text-[#4f5a55] mt-1">
            <span>{data.aggregates.weekly[data.aggregates.weekly.length - 1][0]}</span>
            <span>NIW citation medians recently: {[...data.aggregates.weekly].slice(0, 3).map((w) => Math.round(w[3])).join(" · ")}</span>
            <span>{data.aggregates.weekly[0][0]}</span>
          </div>
        </section>
      )}

      <section className="border border-[--docket] bg-white px-6 py-6 text-center mt-6">
        <h2 className="text-xl mb-2" style={{ fontFamily: "var(--font-serif), serif" }}>
          Like what the data says?
        </h2>
        <p className="text-sm text-[#4f5a55] mb-4 max-w-lg mx-auto">
          Install the free skill and your own AI runs the full evaluation —
          fetching your record, downloading your papers, and folding these
          percentiles into an honest prong-by-prong read.
        </p>
        <a href="/#install" className="btn">Install OpenNIW →</a>
      </section>

      <SiteFooter />
    </div>
  );
}
