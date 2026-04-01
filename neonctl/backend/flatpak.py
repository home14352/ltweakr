import shutil

from neonctl.backend.commands import CommandRunner
from neonctl.backend.models import CommandResult


class FlatpakService:
    def __init__(self) -> None:
        self.runner = CommandRunner()

    def status(self) -> dict:
        has = bool(shutil.which("flatpak"))
        apps = len(self.list_installed()) if has else 0
        return {"supported": has, "installed_apps": apps}

    def list_installed(self) -> list[str]:
        if not shutil.which("flatpak"):
            return []
        res = self.runner.run(["flatpak", "list", "--app", "--columns=application"], timeout=30)
        if res.returncode != 0:
            return []
        return [x for x in res.stdout.splitlines() if x.strip()]

    def search(self, query: str) -> CommandResult:
        if not shutil.which("flatpak"):
            return CommandResult([], 1, "", "flatpak not installed", 0.0)
        return self.runner.run(["flatpak", "search", query], timeout=60)

    def install(self, app_id: str) -> CommandResult:
        if not shutil.which("flatpak"):
            return CommandResult([], 1, "", "flatpak not installed", 0.0)
        return self.runner.run(["flatpak", "install", "-y", app_id], timeout=1800)

    def remove(self, app_id: str) -> CommandResult:
        if not shutil.which("flatpak"):
            return CommandResult([], 1, "", "flatpak not installed", 0.0)
        return self.runner.run(["flatpak", "remove", "-y", app_id], timeout=1800)
