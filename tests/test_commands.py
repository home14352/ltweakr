from neonctl.backend.commands import CommandRunner


def test_command_runner():
    res = CommandRunner().run(["python", "-c", 'print("ok")'])
    assert res.returncode == 0
    assert "ok" in res.stdout
