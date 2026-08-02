"""Local-disk storage adapter (DATA_DIR).

Kept behind one module so a different store can be swapped in later.
"""
import pathlib
import uuid

from ..config import get_settings


def _root() -> pathlib.Path:
    root = pathlib.Path(get_settings().data_dir)
    root.mkdir(parents=True, exist_ok=True)
    return root


def save(case_id: str | None, filename: str, content: bytes) -> str:
    """Store bytes; returns the relative path recorded in the DB."""
    safe_name = filename.replace("/", "_").replace("..", "_")
    rel = pathlib.Path(case_id or "shared") / f"{uuid.uuid4().hex[:8]}_{safe_name}"
    dest = _root() / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(content)
    return str(rel)


def read(rel_path: str) -> bytes:
    path = (_root() / rel_path).resolve()
    if not path.is_relative_to(_root().resolve()):
        raise ValueError("Path escapes storage root")
    return path.read_bytes()
