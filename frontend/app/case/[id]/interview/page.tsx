"use client";
import { useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import Md from "@/components/Md";
import { api } from "@/lib/api";

export default function InterviewPage() {
  const { id } = useParams<{ id: string }>();
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api(`/api/cases/${id}/chat`).then(setMessages).catch(() => {});
  }, [id]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, busy]);

  async function send(text?: string) {
    const content = (text ?? input).trim();
    if (!content || busy) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", content }]);
    setBusy(true);
    try {
      const res = await api(`/api/cases/${id}/chat`, {
        method: "POST",
        body: { content } as any,
      });
      setMessages((m) => [...m, { role: "assistant", content: res.reply }]);
    } catch (e: any) {
      setMessages((m) => [...m, { role: "assistant", content: `⚠️ ${e.message}` }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl mb-2" style={{ fontFamily: "var(--font-serif), serif" }}>
        The interview
      </h1>
      <p className="text-sm text-[#3c4642] mb-6">
        A law firm would send you a 10-page questionnaire. OpenNIW already read
        your record — it only asks what it couldn&apos;t find: your proposed
        endeavor, employment facts, recommender candidates.
      </p>
      <div className="border border-[--rule] bg-white min-h-[45vh] max-h-[60vh] overflow-y-auto px-5 py-4 grid gap-4 content-start">
        {messages.length === 0 && (
          <button className="btn-quiet justify-self-start" onClick={() => send("Hi — I'm ready to start. What do you need from me?")}>
            Start the interview
          </button>
        )}
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "justify-self-end max-w-[85%]" : "max-w-[92%]"}>
            <div className="docket-line text-[#6b7570] mb-1">{m.role === "user" ? "You" : "OpenNIW"}</div>
            <div className={`px-4 py-3 text-sm ${m.role === "user" ? "bg-[--field] border border-[--rule]" : "border-l-2 border-[--docket]"}`}>
              {m.role === "user" ? m.content : <Md>{m.content}</Md>}
            </div>
          </div>
        ))}
        {busy && <div className="drafting-caret docket-line text-[--docket]">Thinking</div>}
        <div ref={endRef} />
      </div>
      <form
        className="mt-3 flex gap-2"
        onSubmit={(e) => {
          e.preventDefault();
          send();
        }}
      >
        <input value={input} onChange={(e) => setInput(e.target.value)}
               placeholder="Answer, or ask anything about your case…" />
        <button className="btn" disabled={busy || !input.trim()}>Send</button>
      </form>
    </div>
  );
}
