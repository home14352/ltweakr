import os


def is_wayland() -> bool:
    return os.environ.get("XDG_SESSION_TYPE") == "wayland"
