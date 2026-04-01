import tomllib
from dataclasses import asdict, dataclass

import tomli_w

from neonctl.backend.paths import config_path
from neonctl.constants import DEFAULT_THEME


@dataclass
class AppSettings:
    theme: str = DEFAULT_THEME
    launch_on_login: bool = False
    start_minimized_to_tray: bool = False
    close_to_tray: bool = True
    tray_monitoring: bool = True
    monitoring_interval_s: int = 5
    show_notifications: bool = True
    restore_window_state: bool = True


class ConfigManager:
    def load(self) -> AppSettings:
        path = config_path()
        if not path.exists():
            return AppSettings()
        data = tomllib.loads(path.read_text())
        return AppSettings(**{**asdict(AppSettings()), **data})

    def save(self, settings: AppSettings) -> None:
        config_path().write_text(tomli_w.dumps(asdict(settings)))
