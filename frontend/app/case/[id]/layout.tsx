"use client";
import { useParams, usePathname } from "next/navigation";

const TABS = [
  ["", "I", "Overview"],
  ["/evidence", "II", "Evidence"],
  ["/interview", "II·b", "Interview"],
  ["/documents", "III", "Documents"],
  ["/forms", "IV–V", "Forms & Package"],
] as const;

export default function CaseLayout({ children }: { children: React.ReactNode }) {
  const { id } = useParams<{ id: string }>();
  const pathname = usePathname();
  const base = `/case/${id}`;

  return (
    <div className="min-h-screen">
      <header className="rule-b bg-white sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-3 flex items-center justify-between">
          <a href="/dashboard" className="docket-line text-[--docket]">← Case files</a>
          <span className="docket-line text-[#6b7570]">OpenNIW</span>
        </div>
        <nav className="max-w-6xl mx-auto px-6 flex gap-1 overflow-x-auto">
          {TABS.map(([suffix, numeral, label]) => {
            const href = base + suffix;
            const active =
              suffix === "" ? pathname === base : pathname.startsWith(href);
            return (
              <a
                key={suffix}
                href={href}
                className={`px-4 py-2.5 text-sm whitespace-nowrap border-b-2 -mb-px transition-colors ${
                  active
                    ? "border-[--docket] text-[--docket] font-medium"
                    : "border-transparent hover:text-[--docket]"
                }`}
              >
                <span className="docket-line mr-2">{numeral}</span>
                {label}
              </a>
            );
          })}
        </nav>
      </header>
      <div className="max-w-6xl mx-auto px-6 py-8">{children}</div>
    </div>
  );
}
