from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from neonctl.backend.desktop import detect_desktop_environment, session_type
from neonctl.backend.distro import detect_distro
from neonctl.backend.monitoring import collect_stats
from neonctl.utils.formatters import human_duration


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.layout.addStretch()
        self.refresh()

    def refresh(self):
        d = detect_distro()
        s = collect_stats()
        self.label.setText(
            f"<h2>Dashboard</h2>"
            f"Distro: {d.name}<br>"
            f"Family: {d.family}<br>"
            f"Desktop: {detect_desktop_environment()} ({session_type()})<br>"
            f"CPU: {s['cpu_percent']}% RAM: {s['ram_percent']}% "
            f"({s['ram_used_gb']}/{s['ram_total_gb']} GB)<br>"
            f"Disk /: {s['disk_root_percent']}% Uptime: {human_duration(s['uptime_s'])}"
        )
