from neonctl.backend.commands import CommandRunner
from neonctl.backend.models import PackageRecord
from neonctl.backend.package_managers import MANAGERS, detect_native_manager


class PackageService:
    def __init__(self) -> None:
        self.runner = CommandRunner()
        self.manager_name = detect_native_manager()

    def manager(self):
        return MANAGERS.get(self.manager_name) if self.manager_name else None

    def search(self, query: str):
        mgr = self.manager()
        if not mgr:
            return []
        return self.runner.run([*mgr.search, query])

    def list_installed(self) -> list[PackageRecord]:
        mgr = self.manager()
        if not mgr:
            return []
        res = self.runner.run(mgr.list_installed, timeout=180)
        if res.returncode != 0:
            return []
        out = []
        for line in res.stdout.splitlines():
            if not line.strip():
                continue
            if "	" in line:
                n, v, *rest = line.split("	")
            else:
                parts = line.split(maxsplit=1)
                n = parts[0]
                v = parts[1] if len(parts) > 1 else "unknown"
                rest = []
            out.append(PackageRecord(name=n, version=v, arch=rest[0] if rest else "unknown"))
        return out
