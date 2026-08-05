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


def test_browser_wording_routes_through_a_command_not_a_pasted_url():
    say = cli._where("intake", URL, "browser")
    assert "browser" in say.lower()
    assert "openniw open" in say, "no tokenless way to reopen the page"


def test_no_host_wording_ever_leaks_the_session_token():
    """The token is a live credential for a server holding the user's whole
    case. Putting it in the sentence the agent speaks would copy it into the
    model's context and every transcript and log downstream."""
    for host in ("desktop", "browser", "embedded"):
        say = cli._where("intake", URL, host)
        assert "token=" not in say, f"{host} wording leaks the token"
        assert "abc" not in say, f"{host} wording leaks the token value"


def test_embedded_wording_is_host_agnostic():
    say = cli._where("forms", URL, "embedded")
    assert "browser" not in say.lower()
    assert "forms" in say


def test_every_host_mentions_how_to_finish():
    for host in ("desktop", "browser", "embedded"):
        assert "'Done'" in cli._where("intake", URL, host), host


SKILL_NAMES = ("niw-petition", "eb1a-petition", "o1-petition",
               "i485-adjustment")


def _skill_text(name):
    import pathlib
    root = pathlib.Path(__file__).resolve().parents[1] / ".agents" / "skills"
    return (root / name / "SKILL.md").read_text(encoding="utf-8")


def test_skills_relay_the_say_line_rather_than_improvising():
    """All four skills must defer to the companion's wording."""
    for skill in SKILL_NAMES:
        text = _skill_text(skill)
        assert "`SAY:` line" in text, f"{skill} does not relay the SAY: line"
        assert "OPENNIW_HOST=desktop" in text, \
            f"{skill} does not know a desktop host can exist"


def test_skills_offer_the_workspace_choice_and_can_set_it_up():
    """The desktop app is source-only, so the agent — which is already the
    installer for the companion — offers it and does the setup."""
    for skill in SKILL_NAMES:
        text = _skill_text(skill)
        assert "Terminal or a window?" in text, f"{skill} never offers the choice"
        assert "npm install" in text, f"{skill} cannot set the window up"
        assert "node --version" in text, f"{skill} does not check for Node"
        # asked once, then remembered
        assert "Decision log" in text and "re-asks" in text, \
            f"{skill} may re-ask the workspace question every session"


def test_the_choice_is_not_offered_when_already_in_the_window():
    """Asking 'terminal or window?' inside the window is nonsense."""
    import re
    for skill in SKILL_NAMES:
        text = _skill_text(skill)
        i = text.find("Terminal or a window?")
        # these files wrap at ~76 columns, so compare on unwrapped text
        section = re.sub(r"\s+", " ", text[i:i + 400])
        assert "ALREADY running inside the desktop app" in section, \
            f"{skill} would ask the question inside the desktop app"
