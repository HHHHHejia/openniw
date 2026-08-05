"""FastAPI app factory + programmatic uvicorn runner for the local UI.

Security posture: binds 127.0.0.1 only; every /api request must carry the
per-session random token (X-OpenNIW-Token header or ?token= query); Host and
Origin are checked; responses are no-store. No accounts — single user on
localhost, but the case folder holds SSN/passport data, so we defend against
other local processes and drive-by browser pages hitting the port.
"""
import hmac
import importlib.resources
import os
import threading
import time

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles

from . import ui_session
from .casefolder import CaseFolder
from .routers import benchmark as benchmark_router
from .routers import citations as citations_router
from .routers import forms as forms_router
from .routers import intake as intake_router
from .routers import meta as meta_router


def _ui_dir():
    try:
        d = importlib.resources.files("openniw") / "ui"
        return d if (d / "index.html").is_file() else None
    except Exception:
        return None


_MISSING_UI = (
    "<!doctype html><meta charset='utf-8'><title>OpenNIW</title>"
    "<body style='font-family:monospace;padding:3rem'>"
    "<h1>OpenNIW API is running</h1>"
    "<p>The browser UI bundle is missing from this install "
    "(dev checkout without a built frontend?). The API works — or run "
    "<code>scripts/build_ui.sh</code> in the repo to build the UI.</p>"
)


def create_app(case_dir, *, token: str, step: str = "forms",
               url: str = "", port: int = 0) -> FastAPI:
    app = FastAPI(title="OpenNIW local companion", docs_url=None,
                  redoc_url=None, openapi_url=None)
    app.state.case = CaseFolder(case_dir)
    app.state.token = token
    app.state.step = step
    app.state.url = url
    app.state.port = port
    app.state.pid = os.getpid()
    app.state.started_at = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    app.state.stop = None  # set by serve()

    @app.middleware("http")
    async def guard(request: Request, call_next):
        host = (request.headers.get("host") or "").split(":")[0]
        if host not in ("127.0.0.1", "localhost"):
            return Response("forbidden host", status_code=403)
        origin = request.headers.get("origin")
        if origin and not origin.startswith(("http://127.0.0.1",
                                            "http://localhost")):
            return Response("forbidden origin", status_code=403)
        if request.url.path.startswith("/api"):
            supplied = (request.headers.get("x-openniw-token")
                        or request.query_params.get("token") or "")
            if not hmac.compare_digest(supplied, app.state.token):
                return Response("missing or bad token", status_code=403)
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        return response

    for r in (meta_router.router, forms_router.router,
              citations_router.router, benchmark_router.router,
              intake_router.router):
        app.include_router(r)

    ui = _ui_dir()
    if ui is not None:
        app.mount("/", StaticFiles(directory=str(ui), html=True), name="ui")
    else:
        @app.get("/")
        def missing_ui() -> Response:
            return Response(_MISSING_UI, media_type="text/html")

    return app


def serve(case_dir, *, step: str, port: int, token: str,
          open_browser: bool = False) -> None:
    """Run the server in the foreground (the `openniw serve` internal mode).

    Writes the sentinel, heartbeats every 15s, and exits when /api/done,
    /api/later, or /api/shutdown fires.
    """
    case = CaseFolder(case_dir)
    url = f"http://127.0.0.1:{port}/{step}/?token={token}"
    app = create_app(case_dir, token=token, step=step, url=url, port=port)

    config = uvicorn.Config(app, host="127.0.0.1", port=port,
                            log_level="warning")
    server = uvicorn.Server(config)
    app.state.stop = lambda: setattr(server, "should_exit", True)

    ui_session.write_sentinel(case, step=step, url=url, port=port,
                              pid=os.getpid(), token=token)

    def heartbeat() -> None:
        while not server.should_exit:
            time.sleep(ui_session.HEARTBEAT_SECONDS)
            sent = ui_session.read_sentinel(case)
            if sent is None or sent.get("status") != "running":
                return  # finalized (done/abandoned) — stop touching it
            ui_session.write_sentinel(
                case, step=step, url=url, port=port, pid=os.getpid(),
                token=token, started_at=sent.get("started_at"),
            )

    threading.Thread(target=heartbeat, daemon=True).start()

    # OPENNIW_NO_BROWSER lets an embedding host (the desktop app) render the
    # page itself: it reads the OPENNIW_URL= line below and loads it in its
    # own view, so popping a system browser would just duplicate the window.
    if open_browser and not os.environ.get("OPENNIW_NO_BROWSER"):
        def _open() -> None:
            time.sleep(0.8)
            import webbrowser
            webbrowser.open(url)
        threading.Thread(target=_open, daemon=True).start()

    print(f"OPENNIW_URL={url}", flush=True)
    server.run()
