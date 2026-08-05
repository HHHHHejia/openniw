// The only bridge between the renderer and the machine. Everything the UI
// can do is enumerated here — there is no filesystem or process access in
// the renderer, and nothing here reads credentials.
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("openniw", {
  detect: () => ipcRenderer.invoke("agent:detect"),

  startAgent: (opts) => ipcRenderer.invoke("agent:start", opts),
  stopAgent: () => ipcRenderer.invoke("agent:stop"),
  sendInput: (data) => ipcRenderer.send("agent:input", data),
  resize: (cols, rows) => ipcRenderer.send("agent:resize", { cols, rows }),

  onAgentData: (cb) => {
    const h = (_e, d) => cb(d);
    ipcRenderer.on("agent:data", h);
    return () => ipcRenderer.removeListener("agent:data", h);
  },
  onAgentExit: (cb) => {
    const h = (_e, code) => cb(code);
    ipcRenderer.on("agent:exit", h);
    return () => ipcRenderer.removeListener("agent:exit", h);
  },
  onCompanionUrl: (cb) => {
    const h = (_e, url) => cb(url);
    ipcRenderer.on("companion:url", h);
    return () => ipcRenderer.removeListener("companion:url", h);
  },
  onCompanionClosed: (cb) => {
    const h = () => cb();
    ipcRenderer.on("companion:closed", h);
    return () => ipcRenderer.removeListener("companion:closed", h);
  },
  watchCase: (dir) => ipcRenderer.invoke("case:watch", dir),

  pickCase: () => ipcRenderer.invoke("case:pick"),
  recentCases: () => ipcRenderer.invoke("case:recents"),
  describeCase: (dir) => ipcRenderer.invoke("case:describe", dir),
  revealCase: (dir) => ipcRenderer.invoke("case:reveal", dir),
  readState: (dir) => ipcRenderer.invoke("case:state", dir),

  evalInfo: () => ipcRenderer.invoke("eval:info"),
  openExternal: (url) => ipcRenderer.invoke("open:external", url),
});
