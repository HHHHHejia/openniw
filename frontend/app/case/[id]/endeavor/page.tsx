"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";

const ELEMENTS: [string, string][] = [
  ["real_world_need", "Real-world need"],
  ["application_scenario", "Application scenario"],
  ["implementation_path", "Implementation path"],
  ["beneficiaries", "Beneficiaries"],
  ["quantifiable_impact", "Quantifiable impact"],
  ["means_of_execution", "Means of execution"],
];

export default function EndeavorPage() {
  const { id } = useParams<{ id: string }>();
  const [e, setE] = useState<any>({});
  const [busy, setBusy] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api(`/api/cases/${id}/endeavor`).then(setE).catch(() => {});
  }, [id]);

  async function save(patch: any) {
    setError("");
    try {
      const res = await api(`/api/cases/${id}/endeavor`, { method: "PUT", body: patch as any });
      setE(res);
      setSaved(true);
      setTimeout(() => setSaved(false), 1200);
    } catch (err: any) {
      setError(err.message);
    }
  }

  async function polish() {
    setBusy(true);
    setError("");
    try {
      await save({ method: e.method, topic: e.topic, impact: e.impact });
      const res = await api(`/api/cases/${id}/endeavor/polish`, { method: "POST" });
      setE(res);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  const composed =
    e.sentence ||
    e.composed ||
    `My proposed endeavor is to ${e.method || "________"} ${e.topic || "________"} in order to ${e.impact || "________"}.`;

  return (
    <div className="max-w-4xl">
      <h1 className="text-2xl mb-2" style={{ fontFamily: "var(--font-serif), serif" }}>
        The endeavor sentence
      </h1>
      <p className="text-sm text-[#3c4642] mb-6 max-w-2xl">
        Your whole petition stands on one sentence, repeated verbatim in every
        document. Once filed it is <strong>frozen</strong> — USCIS treats
        rewording as a potential material change. Compose it carefully here,
        then never touch it again.
      </p>

      {/* Live composed sentence */}
      <div className={`border px-6 py-5 mb-6 bg-white ${e.frozen ? "border-[--docket]" : "border-[--rule]"}`}>
        <div className="docket-line mb-2 flex justify-between">
          <span className={e.frozen ? "text-[--docket]" : ""}>
            {e.frozen ? "FROZEN — cited verbatim in all documents" : "Draft — not yet frozen"}
          </span>
          {saved && <span className="text-[--docket]">saved ✓</span>}
        </div>
        <p className="text-lg leading-relaxed" style={{ fontFamily: "var(--font-serif), serif" }}>
          “{composed}”
        </p>
      </div>

      {!e.frozen && (
        <div className="grid gap-4 mb-6">
          {[
            ["method", "Method / approach", "Active verbs, at most 3 primary methods — e.g. “develop and apply reinforcement learning and formal verification methods”. ≤50 words.", "USCIS reads this as WHAT you do. Too broad reads as unexecutable; too narrow won't survive a project change."],
            ["topic", "Specific topic / focus", "The subject the methods act on — e.g. “to build reliable and energy-efficient autonomous systems”. ≤50 words.", "The topic must sit inside your degree field — the Jan 2025 policy update requires explicit degree–endeavor alignment."],
            ["impact", "Impact / application", "The “in order to …” clause: what it enables for the U.S. — e.g. “strengthen U.S. competitiveness in safety-critical AI across healthcare and energy”. ≤50 words.", "This clause is where Prong 1 (national importance) lives. Tie to named national priorities, not generic economy claims."],
          ].map(([key, label, what, why]) => (
            <label key={key} className="text-sm">
              <span className="docket-line block mb-1">{label}</span>
              <textarea
                rows={2}
                value={e[key] || ""}
                onChange={(ev) => setE({ ...e, [key]: ev.target.value })}
                onBlur={() => save({ [key]: e[key] })}
              />
              <span className="block mt-1 text-xs text-[#4f5a55]"><strong>What:</strong> {what}</span>
              <span className="block text-xs text-[#4f5a55]"><strong>Why we ask:</strong> {why}</span>
            </label>
          ))}
          <div className="flex gap-2">
            <button className="btn" onClick={polish} disabled={busy}>
              {busy ? <span className="drafting-caret">Polishing</span> : "AI polish + score"}
            </button>
          </div>
        </div>
      )}

      {error && <p className="text-sm text-[--stamp] mb-4">{error}</p>}

      {/* Candidates */}
      {!e.frozen && (e.candidates || []).length > 0 && (
        <section className="mb-6">
          <div className="docket-line text-[--docket] mb-2">Polished candidates — pick one</div>
          <div className="grid gap-3">
            {e.candidates.map((c: any, i: number) => (
              <button key={i}
                className={`text-left border px-5 py-4 bg-white hover:border-[--docket] transition-colors ${e.sentence === c.sentence ? "border-[--docket]" : "border-[--rule]"}`}
                onClick={() => save({ sentence: c.sentence, pillars: c.pillars })}>
                <p className="text-sm leading-relaxed" style={{ fontFamily: "var(--font-serif), serif" }}>“{c.sentence}”</p>
                {c.pillars && (
                  <p className="docket-line text-[#4f5a55] mt-2">Pillars: {c.pillars.join(" · ")}</p>
                )}
                {c.rationale && <p className="text-xs text-[#4f5a55] mt-1">{c.rationale}</p>}
              </button>
            ))}
          </div>
        </section>
      )}

      {/* Six-element executability score */}
      {e.element_scores && (
        <section className="mb-6 border border-[--rule] bg-white px-5 py-4">
          <div className="docket-line mb-3">
            Executability check — “a concrete project”, not “a personal plan”
          </div>
          <div className="grid sm:grid-cols-2 gap-2">
            {ELEMENTS.map(([key, label]) => {
              const v = e.element_scores[key] ?? 0;
              const color = v === 2 ? "var(--docket)" : v === 1 ? "#8a7a2a" : "var(--stamp)";
              return (
                <div key={key} className="flex items-center justify-between text-sm border border-[--rule] px-3 py-2">
                  <span>{label}</span>
                  <span className="docket-line" style={{ color }}>
                    {v === 2 ? "evidenced" : v === 1 ? "asserted" : "missing"}
                  </span>
                </div>
              );
            })}
          </div>
          {e.advice && (
            <p className="text-sm mt-3 border-l-2 border-[--docket] pl-3">{e.advice}</p>
          )}
          {(e.element_scores.means_of_execution ?? 0) === 0 && (
            <p className="docket-line text-[--stamp] mt-3">
              ⚠ No means of execution (funding / people / entity / compute / collaborators).
              This is the profile that draws RFEs. Address it before drafting.
            </p>
          )}
        </section>
      )}

      {/* Freeze control */}
      <div className="flex gap-3 items-center">
        {!e.frozen ? (
          <button
            className="btn"
            disabled={!(e.sentence || e.composed)}
            onClick={() => save({ frozen: true })}
          >
            Freeze the endeavor
          </button>
        ) : (
          <button className="btn-quiet" onClick={() => save({ frozen: false })}>
            Unfreeze (before filing only)
          </button>
        )}
        <span className="docket-line text-[#4f5a55]">
          Freezing locks the wording; all drafting cites it verbatim.
        </span>
      </div>
    </div>
  );
}
