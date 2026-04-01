import shutil

from neonctl.backend.commands import CommandRunner
from neonctl.backend.package_managers import detect_native_manager
from neonctl.backend.privileges import PrivilegeManager


class RepositoryService:
    def __init__(self) -> None:
        self.runner = CommandRunner()
        self.priv = PrivilegeManager()

    def status(self) -> dict:
        mgr = detect_native_manager()
        return {"supported": mgr in {"apt", "dnf", "zypper", "pacman"}, "manager": mgr or "none"}

    def list_repos(self) -> list[str]:
        mgr = detect_native_manager()
        if mgr == "apt":
            paths = ["/etc/apt/sources.list", "/etc/apt/sources.list.d"]
            return [p for p in paths if shutil.os.path.exists(p)]
        if mgr == "dnf" and shutil.which("dnf"):
            res = self.runner.run(["dnf", "repolist", "--enabled"], timeout=30)
            return [x for x in res.stdout.splitlines() if x.strip()]
        if mgr == "zypper" and shutil.which("zypper"):
            res = self.runner.run(["zypper", "repos"], timeout=30)
            return [x for x in res.stdout.splitlines() if x.strip()]
        if mgr == "pacman":
            conf = "/etc/pacman.conf"
            if not shutil.os.path.exists(conf):
                return []
            lines = []
            for ln in open(conf, encoding="utf-8", errors="ignore").read().splitlines():
                s = ln.strip()
                if s.startswith("[") and s.endswith("]"):
                    lines.append(s)
            return lines
        return []

    def refresh_metadata(self):
        mgr = detect_native_manager()
        cmd_map = {
            "apt": ["apt", "update"],
            "dnf": ["dnf", "makecache"],
            "zypper": ["zypper", "refresh"],
            "pacman": ["pacman", "-Sy"],
        }
        cmd = cmd_map.get(mgr or "")
        if not cmd:
            return None
        return self.runner.run(self.priv.wrap(cmd), timeout=600)
