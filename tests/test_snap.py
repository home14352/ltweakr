from neonctl.backend.models import CommandResult
from neonctl.backend.snap import SnapService


def test_snap_status():
    assert isinstance(SnapService().status(), dict)


def test_snap_search_when_missing(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: None)
    res = SnapService().search("code")
    assert res.returncode == 1


def test_snap_list_parsing(monkeypatch):
    svc = SnapService()
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/snap")
    output = "Name Version Rev Tracking Publisher Notes\ncode 1 1 stable canonical -\n"
    monkeypatch.setattr(svc.runner, "run", lambda *_a, **_k: CommandResult([], 0, output, "", 0.1))
    assert svc.list_installed() == ["code"]
