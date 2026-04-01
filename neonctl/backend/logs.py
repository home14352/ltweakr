import shutil

from neonctl.backend.commands import CommandRunner


class LogsService:
    def __init__(self) -> None:
        self.runner = CommandRunner()

    def status(self) -> dict:
        has_journalctl = bool(shutil.which("journalctl"))
        source = "journald" if has_journalctl else "unavailable"
        return {"supported": has_journalctl, "source": source}

    def recent(self, lines: int = 50) -> str:
        if not shutil.which("journalctl"):
            return "journalctl unavailable"
        res = self.runner.run(["journalctl", "-n", str(lines), "--no-pager"], timeout=30)
        return res.stdout if res.returncode == 0 else res.stderr
