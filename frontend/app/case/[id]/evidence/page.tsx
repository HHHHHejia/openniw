"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";

const STATUS_STYLE: Record<string, string> = {
  provided: "text-[--docket] border-[--docket]",
  needed: "text-[--stamp] border-[--stamp]",
  suggested: "text-[#6b7570] border-[--rule]",
  na: "text-[#a8a89e] border-[--rule] line-through",
};

export default function EvidencePage() {
  const { id } = useParams<{ id: string }>();
  const [items, setItems] = useState<any[]>([]);
  const [open, setOpen] = useState<string | null>(null);

  const load = () =>
    api(`/api/cases/${id}/evidence`).then(setItems).catch(() => {});
  useEffect(() => {
    load();
  }, [id]);

  async function setStatus(itemId: string, status: string) {
    await api(`/api/cases/${id}/evidence/${itemId}`, {
      method: "PUT",
      body: { status } as any,
    });
    load();
  }

  async function upload(itemId: string, file: File) {
    const form = new FormData();
    form.append("file", file);
    await api(`/api/cases/${id}/evidence/${itemId}/file`, { method: "POST", form });
    load();
  }

  const groups: Record<string, any[]> = {};
  items.forEach((it) => {
    (groups[it.category] ||= []).push(it);
  });
  const provided = items.filter((i) => i.status === "provided").length;

  return (
    <div>
      <div className="flex items-baseline justify-between flex-wrap gap-2 mb-6">
        <h1 className="text-2xl" style={{ fontFamily: "var(--font-serif), serif" }}>
          Evidence ledger
        </h1>
        <span className="docket-line">
          {provided} provided · {items.filter((i) => i.status === "needed").length} needed · {items.length} total
        </span>
      </div>
      <p className="text-sm text-[#3c4642] max-w-2xl mb-8">
        Seeded from your evaluation. Upload a file, or mark items N/A if they
        don&apos;t apply — don&apos;t chase evidence you can&apos;t support. The Index of
        Exhibits will be built only from what&apos;s provided.
      </p>
      <div className="grid gap-8">
        {Object.entries(groups).map(([cat, group]) => (
          <section key={cat}>
            <div className="docket-line text-[--docket] mb-2">{cat.replace(/_/g, " ")}</div>
            <div className="border border-[--rule] bg-white divide-y divide-[--rule]">
              {group.map((it) => (
                <div key={it.id} className="px-5 py-3">
                  <div className="flex items-center justify-between gap-3 flex-wrap">
                    <button
                      className="text-left text-sm font-medium hover:text-[--docket]"
                      onClick={() => setOpen(open === it.id ? null : it.id)}
                    >
                      {it.title}
                    </button>
                    <span className={`docket-line border px-2 py-0.5 ${STATUS_STYLE[it.status] || ""}`}>
                      {it.status}{it.has_file ? " · file ✓" : ""}
                    </span>
                  </div>
                  {open === it.id && (
                    <div className="mt-3 text-sm text-[#3c4642]">
                      {it.description && <p className="mb-2">{it.description}</p>}
                      {it.ai_notes && (
                        <p className="mb-3 border-l-2 border-[--docket] pl-3">{it.ai_notes}</p>
                      )}
                      <div className="flex gap-2 flex-wrap items-center">
                        <label className="btn-quiet !py-1.5 cursor-pointer">
                          Upload file
                          <input type="file" className="hidden !w-auto" onChange={(e) => {
                            const f = e.target.files?.[0];
                            if (f) upload(it.id, f);
                          }} />
                        </label>
                        {["provided", "needed", "na"].map((s) => (
                          <button key={s} className="docket-line px-2 py-1 border border-[--rule] hover:border-[--ink]"
                                  onClick={() => setStatus(it.id, s)}>
                            mark {s}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}
