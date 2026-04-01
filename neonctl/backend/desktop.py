import os


def detect_desktop_environment() -> str:
    return os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION") or "unknown"


def session_type() -> str:
    return os.environ.get("XDG_SESSION_TYPE", "unknown")
