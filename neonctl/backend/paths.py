from pathlib import Path

from neonctl.constants import APP_DIR_NAME, CONFIG_FILE, HISTORY_FILE


def user_config_dir() -> Path:
    return Path.home() / ".config" / APP_DIR_NAME


def user_state_dir() -> Path:
    return Path.home() / ".local" / "state" / APP_DIR_NAME


def ensure_app_dirs() -> None:
    user_config_dir().mkdir(parents=True, exist_ok=True)
    user_state_dir().mkdir(parents=True, exist_ok=True)


def config_path() -> Path:
    ensure_app_dirs()
    return user_config_dir() / CONFIG_FILE


def history_path() -> Path:
    ensure_app_dirs()
    return user_state_dir() / HISTORY_FILE
