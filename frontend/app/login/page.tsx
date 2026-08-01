"use client";
import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { api, setToken } from "@/lib/api";

function LoginInner() {
  const router = useRouter();
  const search = useSearchParams();
  const evalId = search.get("eval");
  const [mode, setMode] = useState<"login" | "register">("register");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const res = await api(`/api/auth/${mode}`, {
        method: "POST",
        body: { email, password } as any,
      });
      setToken(res.token);
      router.push(evalId ? `/dashboard?eval=${evalId}` : "/dashboard");
    } catch (err: any) {
      setError(err.message);
      setBusy(false);
    }
  }

  return (
    <main className="max-w-md mx-auto px-6 py-20">
      <a href="/" className="docket-line text-[--docket]">← OpenNIW</a>
      <div className="mt-8 border border-[--rule] bg-white px-6 py-8">
        <h1 className="text-2xl mb-1" style={{ fontFamily: "var(--font-serif), serif" }}>
          {mode === "register" ? "Create your case file" : "Sign in"}
        </h1>
        <p className="text-sm text-[#3c4642] mb-6">
          {evalId
            ? "Your free evaluation is ready to become a case."
            : "Your data lives only in your own deployment."}
        </p>
        <form onSubmit={submit} className="grid gap-4">
          <label className="text-sm">
            <span className="docket-line block mb-1">Email</span>
            <input required type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
          </label>
          <label className="text-sm">
            <span className="docket-line block mb-1">Password (8+ characters)</span>
            <input required minLength={8} type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </label>
          {error && <p className="text-sm text-[--stamp]">{error}</p>}
          <button className="btn" disabled={busy}>
            {mode === "register" ? "Create account" : "Sign in"}
          </button>
        </form>
        <button
          className="docket-line mt-5 text-[--docket] hover:underline"
          onClick={() => setMode(mode === "register" ? "login" : "register")}
        >
          {mode === "register" ? "Have an account? Sign in" : "New here? Create an account"}
        </button>
      </div>
    </main>
  );
}

export default function Login() {
  return (
    <Suspense>
      <LoginInner />
    </Suspense>
  );
}
