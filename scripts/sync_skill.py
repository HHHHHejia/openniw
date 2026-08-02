#!/usr/bin/env python3
"""Regenerate the skill's fallback scripts from the package sources.

The pip package is the single source of truth; the skill scripts remain as
standalone stdlib fallbacks for offline/sandboxed agents. Shared logic lives
between `# --- BEGIN SYNC: <name>` / `# --- END SYNC: <name>` markers and is
copied verbatim from package source to skill script.

Usage:  python3 scripts/sync_skill.py [--check]
`--check` exits 1 if any skill region differs (used by `make check`).
"""
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
SKILL = REPO / ".agents" / "skills" / "niw-petition" / "scripts"

PAIRS = [
    ("fill maps",
     REPO / "src" / "openniw" / "services" / "formfill.py",
     SKILL / "fill_form.py"),
    ("citation screening",
     REPO / "src" / "openniw" / "services" / "citations_pure.py",
     SKILL / "harvest_citations.py"),
    ("paper download",
     REPO / "src" / "openniw" / "services" / "papers.py",
     SKILL / "fetch_papers.py"),
]


def region(text: str, name: str, path: pathlib.Path) -> tuple[int, int, str]:
    begin = re.search(rf"^# --- BEGIN SYNC: {re.escape(name)}.*$", text, re.M)
    end = re.search(rf"^# --- END SYNC: {re.escape(name)} ---$", text, re.M)
    if not begin or not end:
        raise SystemExit(f"markers for '{name}' not found in {path}")
    return begin.end(), end.start(), text[begin.end():end.start()]


def main() -> int:
    check = "--check" in sys.argv
    dirty = False
    for name, src_path, dst_path in PAIRS:
        src_text = src_path.read_text()
        dst_text = dst_path.read_text()
        _, _, src_region = region(src_text, name, src_path)
        d_start, d_end, dst_region = region(dst_text, name, dst_path)
        if src_region == dst_region:
            print(f"  in sync: {name}")
            continue
        dirty = True
        if check:
            print(f"  DRIFT: {name} ({dst_path.name} != {src_path.name})")
        else:
            dst_path.write_text(dst_text[:d_start] + src_region
                                + dst_text[d_end:])
            print(f"  synced: {name} -> {dst_path.name}")
    if check and dirty:
        print("run: python3 scripts/sync_skill.py")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
