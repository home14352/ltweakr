from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QWidget,
)

from neonctl.backend import autostart
from neonctl.backend.config import ConfigManager
from neonctl.backend.themes import available_themes
from neonctl.constants import ASSETS_DIR


class SettingsPage(QWidget):
    def __init__(self, on_saved=None):
        super().__init__()
        self.on_saved = on_saved
        self.cfg = ConfigManager()
        self.settings = self.cfg.load()
        lay = QFormLayout(self)

        self.theme = QComboBox()
        self.theme.addItems(available_themes())
        self.theme.setCurrentText(self.settings.theme)
        self.launch = QCheckBox()
        self.launch.setChecked(self.settings.launch_on_login)
        self.start_tray = QCheckBox()
        self.start_tray.setChecked(self.settings.start_minimized_to_tray)
        self.close_tray = QCheckBox()
        self.close_tray.setChecked(self.settings.close_to_tray)
        self.monitoring = QCheckBox()
        self.monitoring.setChecked(self.settings.tray_monitoring)
        self.interval = QSpinBox()
        self.interval.setRange(2, 300)
        self.interval.setValue(self.settings.monitoring_interval_s)
        self.save = QPushButton("Save")
        self.save.clicked.connect(self.save_settings)

        lay.addRow("Theme", self.theme)
        lay.addRow("Launch on login", self.launch)
        lay.addRow("Start minimized to tray", self.start_tray)
        lay.addRow("Close to tray", self.close_tray)
        lay.addRow("Enable tray monitoring", self.monitoring)
        lay.addRow("Monitoring interval (s)", self.interval)
        lay.addRow(self.save)

    def _desktop_entry_text(self) -> str:
        desktop_path = ASSETS_DIR / "autostart" / "neonctl.desktop"
        if desktop_path.exists():
            return desktop_path.read_text()
        return (
            "[Desktop Entry]\n"
            "Type=Application\n"
            "Name=NeonCtl\n"
            "Exec=neonctl\n"
            "X-GNOME-Autostart-enabled=true\n"
        )

    def _apply_autostart(self, enabled: bool) -> None:
        if enabled:
            autostart.enable(self._desktop_entry_text())
        else:
            autostart.disable()

    def save_settings(self):
        s = self.settings
        s.theme = self.theme.currentText()
        requested_launch = self.launch.isChecked()
        s.launch_on_login = requested_launch
        s.start_minimized_to_tray = self.start_tray.isChecked()
        s.close_to_tray = self.close_tray.isChecked()
        s.tray_monitoring = self.monitoring.isChecked()
        s.monitoring_interval_s = self.interval.value()

        try:
            self._apply_autostart(requested_launch)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.warning(self, "Autostart error", f"Failed to update autostart: {exc}")
            s.launch_on_login = autostart.is_enabled()
            self.launch.setChecked(s.launch_on_login)

        self.cfg.save(s)
        if self.on_saved:
            self.on_saved(s)

        state = "enabled" if autostart.is_enabled() else "disabled"
        QMessageBox.information(
            self,
            "Settings saved",
            f"Settings updated. Autostart is {state}.",
        )
