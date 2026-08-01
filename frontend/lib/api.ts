const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8400";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("openniw_token");
}

export function setToken(token: string | null) {
  if (token) localStorage.setItem("openniw_token", token);
  else localStorage.removeItem("openniw_token");
}

export async function api(
  path: string,
  opts: RequestInit & { form?: FormData } = {}
): Promise<any> {
  const headers: Record<string, string> = { ...(opts.headers as any) };
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;
  let body = opts.body;
  if (opts.form) {
    body = opts.form;
  } else if (body && typeof body !== "string") {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(body);
  } else if (body) {
    headers["Content-Type"] = "application/json";
  }
  const res = await fetch(`${API}${path}`, { ...opts, headers, body });
  if (res.status === 401 && typeof window !== "undefined") {
    setToken(null);
    if (!path.startsWith("/api/eval")) window.location.href = "/login";
  }
  if (!res.ok) {
    let detail = res.statusText;
    try {
      detail = (await res.json()).detail || detail;
    } catch {}
    throw new Error(detail);
  }
  const type = res.headers.get("content-type") || "";
  if (type.includes("application/json")) return res.json();
  return res.blob();
}

export function downloadUrl(path: string): string {
  return `${API}${path}`;
}

export async function downloadWithAuth(path: string, filename: string) {
  const blob = await api(path);
  const url = URL.createObjectURL(blob as Blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

/** Poll a job until it settles. */
export async function waitForJob(
  jobId: string,
  opts: { public?: boolean; intervalMs?: number; timeoutMs?: number } = {}
): Promise<any> {
  const base = opts.public ? "/api/jobs/public/" : "/api/jobs/";
  const started = Date.now();
  const interval = opts.intervalMs ?? 2500;
  const timeout = opts.timeoutMs ?? 15 * 60 * 1000;
  for (;;) {
    const job = await api(base + jobId);
    if (job.status === "done") return job.result;
    if (job.status === "error") throw new Error(job.error || "Job failed");
    if (Date.now() - started > timeout) throw new Error("Timed out");
    await new Promise((r) => setTimeout(r, interval));
  }
}
