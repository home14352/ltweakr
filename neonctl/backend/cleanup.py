from neonctl.backend.package_managers import detect_native_manager
from neonctl.backend.commands import CommandRunner
from neonctl.backend.privileges import PrivilegeManager


class CleanupService:
    def __init__(self) -> None:
        self.runner = CommandRunner()
        self.priv = PrivilegeManager()

    def status(self) -> dict:
        mgr = detect_native_manager()
        recommendations = []
        if mgr == "apt":
            recommendations.append("apt autoremove")
            recommendations.append("apt clean")
        elif mgr == "dnf":
            recommendations.append("dnf autoremove")
            recommendations.append("dnf clean all")
        elif mgr == "pacman":
            recommendations.append("pacman -Sc")
        return {"supported": True, "manager": mgr or "none", "recommendations": recommendations}

    def run_recommendation(self, command: str):
        parts = command.split()
        if not parts:
            return None
        return self.runner.run(self.priv.wrap(parts), timeout=1800)
