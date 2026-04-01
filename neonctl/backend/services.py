import shutil

from neonctl.backend.commands import CommandRunner
from neonctl.backend.privileges import PrivilegeManager


class ServicesService:
    def __init__(self) -> None:
        self.runner = CommandRunner()
        self.priv = PrivilegeManager()

    def status(self) -> dict:
        has_systemctl = bool(shutil.which("systemctl"))
        failed_units = None
        if has_systemctl:
            res = self.runner.run(["systemctl", "--failed", "--no-legend"], timeout=20)
            if res.returncode == 0:
                failed_units = len([ln for ln in res.stdout.splitlines() if ln.strip()])
        return {
            "supported": has_systemctl,
            "service_manager": "systemd" if has_systemctl else "unavailable",
            "failed_units": failed_units,
        }

    def list_services(self, state: str | None = None) -> list[dict[str, str]]:
        if not shutil.which("systemctl"):
            return []
        cmd = [
            "systemctl",
            "list-units",
            "--type=service",
            "--all",
            "--no-legend",
            "--no-pager",
        ]
        res = self.runner.run(cmd, timeout=60)
        if res.returncode != 0:
            return []

        rows: list[dict[str, str]] = []
        for line in res.stdout.splitlines():
            parts = line.split(None, 4)
            if len(parts) < 4:
                continue
            unit, load, active, sub = parts[:4]
            desc = parts[4] if len(parts) > 4 else ""
            item = {
                "unit": unit,
                "load": load,
                "active": active,
                "sub": sub,
                "description": desc,
            }
            if state == "failed" and active != "failed":
                continue
            if state == "running" and active != "active":
                continue
            rows.append(item)
        return rows

    def manage(self, action: str, unit: str) -> bool:
        if action not in {"start", "stop", "restart", "enable", "disable"}:
            return False
        if not unit.endswith(".service"):
            return False
        cmd = self.priv.wrap(["systemctl", action, unit])
        res = self.runner.run(cmd, timeout=90)
        return res.returncode == 0
