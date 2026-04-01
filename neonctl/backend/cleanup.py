from neonctl.backend.package_managers import detect_native_manager


class CleanupService:
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
