"use client";
import ReactMarkdown from "react-markdown";

export default function Md({ children }: { children: string }) {
  return (
    <div className="prose-doc text-[0.95rem]">
      <ReactMarkdown>{children}</ReactMarkdown>
    </div>
  );
}
