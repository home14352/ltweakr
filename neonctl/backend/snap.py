import shutil

from neonctl.backend.commands import CommandRunner
from neonctl.backend.models import CommandResult


class SnapService:
    def __init__(self) -> None:
        self.runner = CommandRunner()

    def status(self) -> dict:
        has = bool(shutil.which("snap"))
        snaps = len(self.list_installed()) if has else 0
        return {"supported": has, "installed_snaps": snaps}

    def list_installed(self) -> list[str]:
        if not shutil.which("snap"):
            return []
        res = self.runner.run(["snap", "list"], timeout=30)
        if res.returncode != 0:
            return []
        lines = [x for x in res.stdout.splitlines() if x.strip()]
        return [ln.split()[0] for ln in lines[1:]] if len(lines) > 1 else []

    def search(self, query: str) -> CommandResult:
        if not shutil.which("snap"):
            return CommandResult([], 1, "", "snap not installed", 0.0)
        return self.runner.run(["snap", "find", query], timeout=60)

    def install(self, name: str) -> CommandResult:
        if not shutil.which("snap"):
            return CommandResult([], 1, "", "snap not installed", 0.0)
        return self.runner.run(["snap", "install", name], timeout=1800)

    def remove(self, name: str) -> CommandResult:
        if not shutil.which("snap"):
            return CommandResult([], 1, "", "snap not installed", 0.0)
        return self.runner.run(["snap", "remove", name], timeout=1800)
