from neonctl.backend.commands import CommandRunner
from neonctl.backend.package_managers import MANAGERS, detect_native_manager
from neonctl.backend.privileges import PrivilegeManager


class UpdateService:
    def __init__(self) -> None:
        self.runner = CommandRunner()
        self.priv = PrivilegeManager()
        self.manager = detect_native_manager()

    def list_updates(self) -> list[str]:
        if not self.manager:
            return []
        res = self.runner.run(MANAGERS[self.manager].updates, timeout=120)
        if res.returncode != 0:
            return []
        return [ln for ln in res.stdout.splitlines() if ln.strip()]

    def refresh_metadata(self):
        if not self.manager:
            return None
        cmd_map = {
            "apt": ["apt", "update"],
            "dnf": ["dnf", "makecache"],
            "pacman": ["pacman", "-Sy"],
            "zypper": ["zypper", "refresh"],
            "apk": ["apk", "update"],
            "xbps": ["xbps-install", "-S"],
        }
        cmd = cmd_map.get(self.manager)
        if not cmd:
            return None
        return self.runner.run(self.priv.wrap(cmd), timeout=600)
