from neonctl.backend.flatpak import FlatpakService
from neonctl.backend.models import CommandResult


def test_flatpak_status():
    assert isinstance(FlatpakService().status(), dict)


def test_flatpak_search_when_missing(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: None)
    res = FlatpakService().search("vlc")
    assert res.returncode == 1


def test_flatpak_list_parsing(monkeypatch):
    svc = FlatpakService()
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/flatpak")
    monkeypatch.setattr(
        svc.runner,
        "run",
        lambda *_a, **_k: CommandResult([], 0, "org.foo.App\norg.bar.App\n", "", 0.1),
    )
    assert svc.list_installed() == ["org.foo.App", "org.bar.App"]
