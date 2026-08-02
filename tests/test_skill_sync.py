"""Skill fallback scripts must not drift from the package sources."""
import subprocess
import sys
import pathlib
import py_compile

REPO = pathlib.Path(__file__).resolve().parents[1]
SKILL = REPO / ".agents" / "skills" / "niw-petition" / "scripts"


def test_sync_regions_match():
    r = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "sync_skill.py"), "--check"],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_skill_scripts_compile():
    for script in ("fill_form.py", "harvest_citations.py", "fetch_forms.py"):
        py_compile.compile(str(SKILL / script), doraise=True)
