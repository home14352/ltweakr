import shutil

from neonctl.backend.commands import CommandRunner


class SecurityService:
    def __init__(self) -> None:
        self.runner = CommandRunner()

    def _cmd_state(self, cmd: list[str]) -> str:
        res = self.runner.run(cmd, timeout=10)
        return res.stdout.strip() if res.returncode == 0 else "unknown"

    def status(self) -> dict:
        selinux = "unavailable"
        if shutil.which("getenforce"):
            selinux = self._cmd_state(["getenforce"])

        apparmor = "unavailable"
        if shutil.which("aa-status"):
            res = self.runner.run(["aa-status"], timeout=10)
            apparmor = "enabled" if res.returncode == 0 else "disabled_or_unknown"

        firewall = "unknown"
        if shutil.which("firewall-cmd"):
            firewall = self._cmd_state(["firewall-cmd", "--state"])
        elif shutil.which("ufw"):
            firewall = self._cmd_state(["ufw", "status"])

        return {
            "supported": True,
            "selinux": selinux,
            "apparmor": apparmor,
            "firewall": firewall,
        }
