// Same-origin client for the openniw local companion. The per-session token
// arrives in the launch URL (?token=...) and is kept in sessionStorage so
// tab navigation keeps working.

export function getToken(): string {
  if (typeof window === "undefined") return "";
  const fromUrl = new URLSearchParams(window.location.search).get("token");
  if (fromUrl) {
    sessionStorage.setItem("openniw_token", fromUrl);
    return fromUrl;
  }
  return sessionStorage.getItem("openniw_token") || "";
}

export function withToken(path: string): string {
  const t = getToken();
  return t ? `${path}${path.includes("?") ? "&" : "?"}token=${t}` : path;
}

export async function api(path: string, opts: { method?: string; body?: any } = {}) {
  const res = await fetch(path, {
    method: opts.method || "GET",
    headers: {
      "X-OpenNIW-Token": getToken(),
      ...(opts.body !== undefined ? { "Content-Type": "application/json" } : {}),
    },
    body: opts.body !== undefined ? JSON.stringify(opts.body) : undefined,
  });
  if (!res.ok) {
    let detail = `${res.status}`;
    try {
      detail = (await res.json()).detail || detail;
    } catch {}
    const err: any = new Error(detail);
    err.status = res.status;
    throw err;
  }
  const ct = res.headers.get("content-type") || "";
  return ct.includes("application/json") ? res.json() : res.blob();
}

export async function download(path: string, filename: string) {
  const blob = (await api(path)) as Blob;
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
