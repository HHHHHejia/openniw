"""The case folder is the only storage. This module is the storage layer.

Atomic writes (tmp + os.replace), mtime_ns optimistic-concurrency versions,
an append-only events log, and the UI-session sentinel location.
"""
import json
import os
import pathlib
import tempfile
import time
from typing import Any


class Conflict(Exception):
    """Optimistic-concurrency failure: file changed since base_version."""


class CaseFolder:
    def __init__(self, root: pathlib.Path | str):
        self.root = pathlib.Path(root).resolve()

    # ---- well-known paths -------------------------------------------------
    @property
    def state_md(self) -> pathlib.Path:
        return self.root / "STATE.md"

    @property
    def case_json(self) -> pathlib.Path:
        return self.root / "case.json"

    @property
    def answers(self) -> pathlib.Path:
        return self.root / "forms" / "answers.json"

    @property
    def answers_meta(self) -> pathlib.Path:
        return self.root / "forms" / "answers.meta.json"

    @property
    def fill_report(self) -> pathlib.Path:
        return self.root / "forms" / "fill-report.json"

    @property
    def blank_dir(self) -> pathlib.Path:
        return self.root / "forms" / "blank"

    @property
    def forms_dir(self) -> pathlib.Path:
        return self.root / "forms"

    @property
    def scored(self) -> pathlib.Path:
        return self.root / "citations" / "scored.json"

    @property
    def selection(self) -> pathlib.Path:
        return self.root / "citations" / "selection.json"

    @property
    def meta_dir(self) -> pathlib.Path:
        return self.root / ".openniw"

    @property
    def sentinel(self) -> pathlib.Path:
        return self.meta_dir / "ui-session.json"

    @property
    def events(self) -> pathlib.Path:
        return self.meta_dir / "events.jsonl"

    @property
    def server_log(self) -> pathlib.Path:
        return self.meta_dir / "server.log"

    # ---- json io ----------------------------------------------------------
    def version(self, path: pathlib.Path) -> int:
        try:
            return path.stat().st_mtime_ns
        except FileNotFoundError:
            return 0

    def read_json(self, path: pathlib.Path, default: Any = None
                  ) -> tuple[Any, int]:
        """Returns (data, version). version==0 means the file doesn't exist."""
        try:
            raw = path.read_text()
        except FileNotFoundError:
            return (default if default is not None else {}), 0
        return json.loads(raw), self.version(path)

    def write_json(self, path: pathlib.Path, data: Any,
                   base_version: int | None = None) -> int:
        """Atomic write. If base_version is given and stale, raises Conflict.
        Returns the new version."""
        if base_version is not None and self.version(path) != base_version:
            raise Conflict(f"{path.name} changed on disk")
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(path.parent),
                                   prefix=f".{path.name}.", suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(data, f, indent=1, ensure_ascii=False)
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
        return self.version(path)

    def append_event(self, event: str, **fields: Any) -> None:
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "event": event,
               **fields}
        with open(self.events, "a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
