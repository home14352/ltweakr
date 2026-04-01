import shutil

from neonctl.backend.commands import CommandRunner
from neonctl.backend.package_managers import detect_native_manager


class RepositoryService:
    def __init__(self) -> None:
        self.runner = CommandRunner()

    def status(self) -> dict:
        mgr = detect_native_manager()
        return {"supported": mgr in {"apt", "dnf", "zypper"}, "manager": mgr or "none"}

    def list_repos(self) -> list[str]:
        mgr = detect_native_manager()
        if mgr == "apt":
            paths = ["/etc/apt/sources.list"]
            return [p for p in paths if shutil.os.path.exists(p)]
        if mgr == "dnf" and shutil.which("dnf"):
            res = self.runner.run(["dnf", "repolist", "--enabled"], timeout=30)
            return [x for x in res.stdout.splitlines() if x.strip()]
        if mgr == "zypper" and shutil.which("zypper"):
            res = self.runner.run(["zypper", "repos"], timeout=30)
            return [x for x in res.stdout.splitlines() if x.strip()]
        return []
