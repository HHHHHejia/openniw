"""Where a browser step opens is knowable only by the companion, so the
companion — not the agent — writes the sentence the user reads. If this
contract slips, a desktop user gets told to "open your browser" for a page
that is already on screen beside them.
"""
import importlib

cli = importlib.import_module("openniw.cli")


def test_host_defaults_to_browser(monkeypatch):
    monkeypatch.delenv("OPENNIW_HOST", raising=False)
    monkeypatch.delenv("OPENNIW_NO_BROWSER", raising=False)
    assert cli._host() == "browser"


def test_embedding_host_declares_itself(monkeypatch):
    monkeypatch.setenv("OPENNIW_HOST", "desktop")
    assert cli._host() == "desktop"
    monkeypatch.setenv("OPENNIW_HOST", "DeskTop")   # case-insensitive
    assert cli._host() == "desktop"


def test_browser_suppressed_without_a_named_host(monkeypatch):
    """Something is embedding us, but did not say what it is."""
    monkeypatch.delenv("OPENNIW_HOST", raising=False)
    monkeypatch.setenv("OPENNIW_NO_BROWSER", "1")
    assert cli._host() == "embedded"


def test_unknown_host_value_falls_back(monkeypatch):
    monkeypatch.setenv("OPENNIW_HOST", "nonsense")
    monkeypatch.delenv("OPENNIW_NO_BROWSER", raising=False)
    assert cli._host() == "browser"


URL = "http://127.0.0.1:5000/intake/?token=abc"


def test_desktop_wording_never_sends_anyone_to_a_browser():
    say = cli._where("intake", URL, "desktop")
    assert "browser" not in say.lower().replace("no browser needed", "")
    assert "panel" in say
    assert URL not in say          # the URL is noise when the page is on screen


def test_browser_wording_gives_the_address():
    say = cli._where("intake", URL, "browser")
    assert URL in say and "browser" in say.lower()


def test_embedded_wording_is_host_agnostic():
    say = cli._where("forms", URL, "embedded")
    assert "browser" not in say.lower()
    assert "forms" in say


def test_every_host_mentions_how_to_finish():
    for host in ("desktop", "browser", "embedded"):
        assert "'Done'" in cli._where("intake", URL, host), host


def test_skills_relay_the_say_line_rather_than_improvising():
    """All four skills must defer to the companion's wording."""
    import pathlib
    root = pathlib.Path(__file__).resolve().parents[1] / ".agents" / "skills"
    for skill in ("niw-petition", "eb1a-petition", "o1-petition",
                  "i485-adjustment"):
        text = (root / skill / "SKILL.md").read_text(encoding="utf-8")
        assert "`SAY:` line" in text, f"{skill} does not relay the SAY: line"
        assert "OPENNIW_HOST=desktop" in text, \
            f"{skill} does not know a desktop host can exist"
