from neonctl.backend.models import CommandResult
from neonctl.backend.processes import ProcessesService


def test_processes_status_shape():
    s = ProcessesService().status()
    assert "supported" in s


def test_clean_ram_calls_runner(monkeypatch):
    svc = ProcessesService()
    monkeypatch.setattr(svc.priv, "wrap", lambda cmd: cmd)
    monkeypatch.setattr(
        svc.runner,
        "run",
        lambda *_a, **_k: CommandResult([], 0, "ok", "", 0.1),
    )
    assert svc.clean_ram() is True
