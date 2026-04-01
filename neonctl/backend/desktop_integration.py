from pathlib import Path


def desktop_entry_target() -> Path:
    return Path.home() / ".local" / "share" / "applications" / "neonctl.desktop"


def icon_target() -> Path:
    return (
        Path.home() / ".local" / "share" / "icons" / "hicolor" / "256x256" / "apps" / "neonctl.png"
    )


def integration_status() -> dict:
    return {"desktop": desktop_entry_target().exists(), "icon": icon_target().exists()}
