"""Prompt template loader. Templates are markdown files in this package."""
import pathlib

_DIR = pathlib.Path(__file__).parent


def load(name: str) -> str:
    return (_DIR / f"{name}.md").read_text()
