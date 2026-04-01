from pathlib import Path


def read_text_safe(path: Path) -> str:
    try:
        return path.read_text()
    except Exception:
        return ""
