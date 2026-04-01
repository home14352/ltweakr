from neonctl.backend.models import CommandResult
from neonctl.backend.services import ServicesService


def test_services_status():
    assert "supported" in ServicesService().status()


def test_list_services_parsing(monkeypatch):
    svc = ServicesService()
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/systemctl")

    sample = (
        "ssh.service loaded active running OpenSSH server daemon\n"
        "foo.service loaded failed failed Foo"
    )

    monkeypatch.setattr(
        svc.runner,
        "run",
        lambda *_args, **_kwargs: CommandResult([], 0, sample, "", 0.1),
    )

    running = svc.list_services(state="running")
    failed = svc.list_services(state="failed")
    assert len(running) == 1
    assert len(failed) == 1


def test_manage_rejects_invalid_unit():
    svc = ServicesService()
    assert svc.manage("restart", "not-a-service") is False
