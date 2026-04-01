from pathlib import Path

from neonctl.constants import ASSETS_DIR


def theme_path(theme_name: str) -> Path:
    return ASSETS_DIR / "qss" / f"{theme_name}.qss"


def available_themes() -> list[str]:
    return ["cyberpunk_dark", "terminal_green", "neon_purple", "amber_tactical", "ice_blue_matrix"]
