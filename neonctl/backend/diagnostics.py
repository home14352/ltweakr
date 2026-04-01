import shutil

from neonctl.backend.capabilities import detect_capabilities


def run_checks() -> list[dict]:
    caps = detect_capabilities()
    checks = []
    checks.append(
        {
            "name": "native_manager",
            "ok": caps.native_manager != "none",
            "detail": caps.native_manager,
        }
    )
    checks.append(
        {"name": "flatpak", "ok": bool(shutil.which("flatpak")), "detail": "flatpak binary"}
    )
    checks.append({"name": "snap", "ok": bool(shutil.which("snap")), "detail": "snap binary"})
    checks.append(
        {"name": "systemctl", "ok": bool(shutil.which("systemctl")), "detail": "service manager"}
    )
    return checks
