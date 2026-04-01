from __future__ import annotations

import shutil

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

    def aur_helpers(self) -> list[str]:
        helpers = ["yay", "paru", "pikaur", "trizen"]
        return [h for h in helpers if shutil.which(h)]

    def default_aur_helper(self) -> str | None:
        helpers = self.aur_helpers()
        return helpers[0] if helpers else None

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

    def aur_search(self, query: str, helper: str) -> CommandResult:
        if not shutil.which(helper):
            return CommandResult([helper], 1, "", f"AUR helper {helper} not found", 0.0)
        return self.runner.run([helper, "-Ss", query], timeout=180)

    def aur_install(self, package_name: str, helper: str) -> CommandResult:
        if not shutil.which(helper):
            return CommandResult([helper], 1, "", f"AUR helper {helper} not found", 0.0)
        if not valid_package_name(package_name):
            return CommandResult([], 2, "", f"Invalid package name: {package_name}", 0.0)
        return self.runner.run([helper, "-S", "--noconfirm", package_name], timeout=1800)
