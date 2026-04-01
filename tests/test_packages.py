from neonctl.backend.models import CommandResult
from neonctl.backend.packages import PackageService


def test_package_service_instantiates():
    svc = PackageService()
    assert svc is not None


def test_install_rejects_invalid_name():
    svc = PackageService()
    res = svc.install("bad package name", elevated=False)
    assert res.returncode == 2


def test_remove_invokes_runner(monkeypatch):
    svc = PackageService()

    class DummyManager:
        remove = ["apt", "remove", "-y"]

    svc.manager = lambda: DummyManager()  # type: ignore[assignment]
    called = {}

    def fake_run(cmd, timeout=60):
        called["cmd"] = cmd
        return CommandResult(command=cmd, returncode=0, stdout="ok", stderr="", duration_s=0.1)

    monkeypatch.setattr(svc.runner, "run", fake_run)
    res = svc.remove("nano", elevated=False)
    assert res.returncode == 0
    assert called["cmd"][-1] == "nano"
