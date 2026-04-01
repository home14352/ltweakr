from neonctl.backend.models import CapabilityMatrix
from neonctl.backend.package_managers import detect_native_manager
from neonctl.backend.privileges import PrivilegeManager


def detect_capabilities() -> CapabilityMatrix:
    mgr = detect_native_manager() or "none"
    pkg_actions = {
        "search": mgr != "none",
        "install": mgr != "none",
        "remove": mgr != "none",
        "reinstall": mgr in {"apt", "dnf", "pacman"},
        "updates": mgr != "none",
    }
    svc = {"list": True, "start": True, "stop": True, "enable": True, "disable": True}
    methods = PrivilegeManager().available_methods()
    notes = [] if mgr != "none" else ["No supported native package manager detected"]
    return CapabilityMatrix(
        native_manager=mgr,
        package_actions=pkg_actions,
        service_actions=svc,
        privilege_methods=methods,
        notes=notes,
    )
