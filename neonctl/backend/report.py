from datetime import datetime

from neonctl.backend.capabilities import detect_capabilities
from neonctl.backend.distro import detect_distro


def diagnostics_report() -> str:
    d = detect_distro()
    c = detect_capabilities()
    lines = [
        f"NeonCtl Diagnostics Report - {datetime.utcnow().isoformat()}Z",
        f"Distro: {d.name} ({d.distro_id}) {d.version}",
        f"Native manager: {c.native_manager}",
        f"Privilege methods: {', '.join(c.privilege_methods) or 'none'}",
        "Package actions:",
    ]
    lines.extend([f"  - {k}: {v}" for k, v in c.package_actions.items()])
    if c.notes:
        lines.append("Notes:")
        lines.extend([f"  - {n}" for n in c.notes])
    return "\n".join(lines)
