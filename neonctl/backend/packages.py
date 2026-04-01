from __future__ import annotations

from neonctl.backend.commands import CommandRunner
from neonctl.backend.models import CommandResult, PackageRecord
from neonctl.backend.package_managers import MANAGERS, detect_native_manager
from neonctl.backend.privileges import PrivilegeManager
from neonctl.backend.validators import valid_package_name


class PackageService:
    def __init__(self) -> None:
        self.runner = CommandRunner()
        self.privileges = PrivilegeManager()
        self.manager_name = detect_native_manager()

    def manager(self):
        return MANAGERS.get(self.manager_name) if self.manager_name else None

    def _unsupported(self, action: str) -> CommandResult:
        return CommandResult(
            command=[action],
            returncode=1,
            stdout="",
            stderr="No supported native package manager detected.",
            duration_s=0.0,
        )

    def search(self, query: str) -> CommandResult:
        mgr = self.manager()
        if not mgr:
            return self._unsupported("search")
        return self.runner.run([*mgr.search, query])

    def install(self, package_name: str, elevated: bool = True) -> CommandResult:
        mgr = self.manager()
        if not mgr:
            return self._unsupported("install")
        if not valid_package_name(package_name):
            return CommandResult([], 2, "", f"Invalid package name: {package_name}", 0.0)
        cmd = [*mgr.install, package_name]
        if elevated:
            cmd = self.privileges.wrap(cmd)
        return self.runner.run(cmd, timeout=1800)

    def remove(self, package_name: str, elevated: bool = True) -> CommandResult:
        mgr = self.manager()
        if not mgr:
            return self._unsupported("remove")
        if not valid_package_name(package_name):
            return CommandResult([], 2, "", f"Invalid package name: {package_name}", 0.0)
        cmd = [*mgr.remove, package_name]
        if elevated:
            cmd = self.privileges.wrap(cmd)
        return self.runner.run(cmd, timeout=1800)

    def list_installed(self) -> list[PackageRecord]:
        mgr = self.manager()
        if not mgr:
            return []
        res = self.runner.run(mgr.list_installed, timeout=180)
        if res.returncode != 0:
            return []
        out: list[PackageRecord] = []
        for line in res.stdout.splitlines():
            if not line.strip():
                continue
            if "\t" in line:
                name, version, *rest = line.split("\t")
            else:
                parts = line.split(maxsplit=1)
                name = parts[0]
                version = parts[1] if len(parts) > 1 else "unknown"
                rest = []
            out.append(
                PackageRecord(
                    name=name,
                    version=version,
                    arch=rest[0] if rest else "unknown",
                )
            )
        return out
