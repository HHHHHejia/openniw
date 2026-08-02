"""The `openniw` command-line interface.

Browser sessions:
    openniw ui forms|citations [--case DIR] [--no-open]
    openniw status | wait [--timeout S] | stop        (sentinel verdicts)
Headless deterministic compute (same reports as the API):
    openniw fill <code|all> · package · harvest "Title" … · fetch-forms ·
    docx <md> · highlight <pdf> --needle …
"""
import argparse
import json
import os
import pathlib
import secrets
import socket
import subprocess
import sys
import urllib.request

from . import __version__, ui_session
from .casefolder import CaseFolder

STEPS = ("forms", "citations", "benchmark")


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _cmd_ui(ns) -> int:
    case = CaseFolder(ns.case)
    code, sent = ui_session.status(case)
    if code == ui_session.LIVE:
        print(f"A browser session is already open: {sent['url']}")
        print(f"OPENNIW_URL={sent['url']}")
        if not ns.no_open:
            import webbrowser
            webbrowser.open(sent["url"])
        return 5
    if code == ui_session.STALE:
        case.sentinel.unlink(missing_ok=True)  # dead server; reclaim

    port = ns.port or _free_port()
    token = secrets.token_hex(16)
    log = open(case.server_log, "a") if case.meta_dir.is_dir() else None
    if log is None:
        case.meta_dir.mkdir(parents=True, exist_ok=True)
        log = open(case.server_log, "a")
    proc = subprocess.Popen(
        [sys.executable, "-m", "openniw.cli", "serve",
         "--case", str(case.root), "--step", ns.step, "--port", str(port),
         "--token", token] + ([] if ns.no_open else ["--open-browser"]),
        stdout=log, stderr=log, start_new_session=True,
    )
    url = f"http://127.0.0.1:{port}/{ns.step}/?token={token}"
    print(f"OpenNIW {ns.step} session: {url}")
    print(f"Server started (pid {proc.pid}); it keeps running even if this "
          "terminal closes. Finish with the page's 'Done' button.")
    print(f"OPENNIW_URL={url}")
    if os.environ.get("SSH_CONNECTION") or os.environ.get("SSH_TTY"):
        print(f"Remote session? Forward the port: "
              f"ssh -L {port}:127.0.0.1:{port} <host> — then open the URL "
              "locally.")
    return 0


def _cmd_serve(ns) -> int:
    from .server import serve
    serve(ns.case, step=ns.step, port=ns.port, token=ns.token,
          open_browser=ns.open_browser)
    return 0


def _cmd_status(ns) -> int:
    case = CaseFolder(ns.case)
    code, detail = ui_session.status(case)
    print(json.dumps(detail, ensure_ascii=False))
    return code


def _cmd_wait(ns) -> int:
    case = CaseFolder(ns.case)
    code, detail = ui_session.wait(case, timeout=ns.timeout)
    print(json.dumps(detail, ensure_ascii=False))
    return code


def _cmd_stop(ns) -> int:
    case = CaseFolder(ns.case)
    code, sent = ui_session.status(case)
    if code != ui_session.LIVE:
        print("no live session")
        return code
    try:
        req = urllib.request.Request(
            f"http://127.0.0.1:{sent['port']}/api/shutdown", method="POST",
            headers={"X-OpenNIW-Token": sent["token"]})
        urllib.request.urlopen(req, timeout=5)
        print("stopped")
        return 0
    except Exception as exc:
        print(f"stop failed: {exc}")
        return 1


def _cmd_fill(ns) -> int:
    from .services import formfill
    case = CaseFolder(ns.case)
    answers, _ = case.read_json(case.answers)
    if not answers:
        print("forms/answers.json is empty — nothing to fill", file=sys.stderr)
        return 2
    codes = list(formfill.FORM_SOURCES) if ns.form == "all" else [ns.form]
    reports = {}
    rc = 0
    for code in codes:
        try:
            pdf, report = formfill.fill(code, answers, case.blank_dir)
        except FileNotFoundError as exc:
            print(f"{code}: {exc}", file=sys.stderr)
            rc = 2
            continue
        out = case.forms_dir / f"{code}-filled.pdf"
        out.write_bytes(pdf)
        reports[code] = report
        print(f"{code}: {report['filled']} fields filled, "
              f"{len(report['unmatched_fields'])} unmatched -> {out}")
        for w in report["warnings"]:
            print(f"  warning: {w}")
    existing, _ = case.read_json(case.fill_report)
    existing.update(reports)
    case.write_json(case.fill_report, existing)
    print(json.dumps(reports, ensure_ascii=False))
    print("PRINT the filled forms and verify every page on paper before "
          "signing — do not trust a single on-screen viewer.")
    return rc


def _cmd_package(ns) -> int:
    from .services import package_zip
    case = CaseFolder(ns.case)
    data = package_zip.build_package(case.root)
    out = case.root / "package" / "openniw-package.zip"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print(f"package -> {out} ({len(data) // 1024} KB)")
    return 0


def _cmd_harvest(ns) -> int:
    from .services.harvest import harvest
    summary = harvest(ns.titles, pathlib.Path(ns.out),
                      max_per_work=ns.max_per_work)
    print(json.dumps(summary, ensure_ascii=False))
    return 0


def _cmd_papers(ns) -> int:
    from .services.papers import download_papers
    summary = download_papers(ns.titles, pathlib.Path(ns.out))
    print(json.dumps(summary, ensure_ascii=False))
    if summary["preprint_only"]:
        print(f"NOTE: {summary['preprint_only']} paper(s) only available as "
              "preprints — the officially published version is the preferred "
              "exhibit; ask the user to supply it (institutional access).")
    return 0 if summary["downloaded"] or not ns.titles else 1


def _cmd_fetch_forms(ns) -> int:
    from .services.fetch_forms import fetch_forms
    case = CaseFolder(ns.case)
    result = fetch_forms(case.blank_dir)
    return 1 if result["failed"] else 0


def _cmd_docx(ns) -> int:
    from .services import docx_export
    src = pathlib.Path(ns.markdown)
    out = pathlib.Path(ns.out) if ns.out else src.with_suffix(".docx")
    out.write_bytes(docx_export.markdown_to_docx(src.read_text()))
    print(f"docx -> {out}")
    return 0


def _cmd_highlight(ns) -> int:
    from .services.citations_pure import highlight_pdf
    src = pathlib.Path(ns.pdf)
    out = pathlib.Path(ns.out) if ns.out else src.with_name(
        src.stem + "-highlighted.pdf")
    out.write_bytes(highlight_pdf(src.read_bytes(), ns.needle))
    print(f"highlighted -> {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="openniw",
        description="OpenNIW local companion: browser UI + deterministic "
                    "compute over a NIW case folder. No accounts, no "
                    "database, no API keys.")
    ap.add_argument("--version", action="version",
                    version=f"openniw {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def _case_arg(p):
        p.add_argument("--case", default=".",
                       help="case folder (default: current directory)")

    p = sub.add_parser("ui", help="open a browser session (detached server)")
    p.add_argument("step", choices=STEPS)
    _case_arg(p)
    p.add_argument("--port", type=int, default=0)
    p.add_argument("--no-open", action="store_true")
    p.set_defaults(fn=_cmd_ui)

    p = sub.add_parser("serve", help="run the server in the foreground")
    p.add_argument("--step", choices=STEPS, default="forms")
    _case_arg(p)
    p.add_argument("--port", type=int, required=True)
    p.add_argument("--token", required=True)
    p.add_argument("--open-browser", action="store_true")
    p.set_defaults(fn=_cmd_serve)

    p = sub.add_parser("status", help="UI-session verdict "
                       "(exit: 0 live, 2 done, 3 abandoned, 4 stale, 6 none)")
    _case_arg(p)
    p.set_defaults(fn=_cmd_status)

    p = sub.add_parser("wait", help="block until the session finishes")
    _case_arg(p)
    p.add_argument("--timeout", type=float, default=540.0)
    p.set_defaults(fn=_cmd_wait)

    p = sub.add_parser("stop", help="gracefully stop a live session")
    _case_arg(p)
    p.set_defaults(fn=_cmd_stop)

    p = sub.add_parser("fill", help="fill official PDFs from answers.json")
    p.add_argument("form", help="i-140 | eta-9089-appendix-a | "
                   "eta-9089-final-determination | g-1145 | all")
    _case_arg(p)
    p.set_defaults(fn=_cmd_fill)

    p = sub.add_parser("package", help="assemble the filing-package ZIP")
    _case_arg(p)
    p.set_defaults(fn=_cmd_package)

    p = sub.add_parser("harvest", help="harvest citing papers from OpenAlex")
    p.add_argument("titles", nargs="+")
    p.add_argument("--out", default="citations/harvest.json")
    p.add_argument("--max-per-work", type=int, default=200)
    p.set_defaults(fn=_cmd_harvest)

    p = sub.add_parser("papers",
                       help="batch-download the applicant's own papers "
                            "(OpenAlex -> arXiv/PMC/publisher OA PDFs)")
    p.add_argument("titles", nargs="+")
    p.add_argument("--out", default="sources/papers")
    p.set_defaults(fn=_cmd_papers)

    p = sub.add_parser("fetch-forms", help="download official blank PDFs")
    _case_arg(p)
    p.set_defaults(fn=_cmd_fetch_forms)

    p = sub.add_parser("docx", help="render a markdown document to DOCX")
    p.add_argument("markdown")
    p.add_argument("--out")
    p.set_defaults(fn=_cmd_docx)

    p = sub.add_parser("highlight", help="highlight needles in a PDF")
    p.add_argument("pdf")
    p.add_argument("--needle", action="append", required=True)
    p.add_argument("--out")
    p.set_defaults(fn=_cmd_highlight)

    ns = ap.parse_args(argv)
    return ns.fn(ns)


if __name__ == "__main__":
    raise SystemExit(main())
