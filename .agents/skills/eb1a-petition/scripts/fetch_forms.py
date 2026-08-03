#!/usr/bin/env python3
"""Download the official USCIS form PDFs into ./forms/blank/.

Stdlib only. Browser-style headers are sent to avoid bot blocks.
EB-1A files no DOL paperwork, so no ETA-9089 PDFs are fetched.
Usage:  python3 fetch_forms.py [dest_dir]
"""
import pathlib
import sys
import urllib.request

FORMS = {
    "i-140.pdf": "https://www.uscis.gov/sites/default/files/document/forms/i-140.pdf",
    "i-907.pdf": "https://www.uscis.gov/sites/default/files/document/forms/i-907.pdf",
    "g-1145.pdf": "https://www.uscis.gov/sites/default/files/document/forms/g-1145.pdf",
    "g-1450.pdf": "https://www.uscis.gov/sites/default/files/document/forms/g-1450.pdf",
    "g-1650.pdf": "https://www.uscis.gov/sites/default/files/document/forms/g-1650.pdf",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def main() -> int:
    dest = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "forms/blank")
    dest.mkdir(parents=True, exist_ok=True)
    failures = 0
    for name, url in FORMS.items():
        target = dest / name
        if target.exists() and target.stat().st_size > 10000:
            print(f"  exists  {name}")
            continue
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            if not data.startswith(b"%PDF"):
                raise ValueError("response is not a PDF (blocked?)")
            target.write_bytes(data)
            print(f"  fetched {name} ({len(data) // 1024} KB)")
        except Exception as exc:
            failures += 1
            print(f"  FAILED  {name}: {exc}")
    if failures:
        print(f"\n{failures} download(s) failed. Fetch the failed PDFs with "
              "your agent's own web tool, or download them in a browser "
              "from uscis.gov/forms into the dest dir.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
