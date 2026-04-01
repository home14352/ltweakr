from pathlib import Path


def autostart_path() -> Path:
    return Path.home() / ".config" / "autostart" / "neonctl.desktop"


def is_enabled() -> bool:
    return autostart_path().exists()


def enable(desktop_entry: str) -> None:
    path = autostart_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(desktop_entry)


def disable() -> None:
    p = autostart_path()
    if p.exists():
        p.unlink()
