from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QSystemTrayIcon

from neonctl.backend.monitoring import collect_stats
from neonctl.utils.formatters import human_duration


class NeonTray:
    def __init__(self, icon, parent, open_page_cb, settings):
        self.tray = QSystemTrayIcon(icon, parent)
        self.menu = QMenu()
        self.menu.addAction(QAction("Show", parent, triggered=parent.showNormal))
        self.menu.addAction(
            QAction("Dashboard", parent, triggered=lambda: open_page_cb("Dashboard"))
        )
        self.menu.addAction(QAction("Packages", parent, triggered=lambda: open_page_cb("Packages")))
        self.menu.addAction(QAction("Updates", parent, triggered=lambda: open_page_cb("Updates")))
        self.menu.addAction(
            QAction("Diagnostics", parent, triggered=lambda: open_page_cb("Diagnostics"))
        )
        self.menu.addSeparator()
        self.menu.addAction(QAction("Quit", parent, triggered=parent.force_quit))
        self.tray.setContextMenu(self.menu)
        self.timer = QTimer(parent)
        self.timer.timeout.connect(self.refresh_tooltip)
        self.timer.start(max(2000, settings.monitoring_interval_s * 1000))

    def show(self):
        self.tray.show()
        self.refresh_tooltip()

    def refresh_tooltip(self):
        s = collect_stats()
        self.tray.setToolTip(
            f"CPU {s['cpu_percent']}% | RAM {s['ram_percent']}% "
            f"({s['ram_used_gb']}/{s['ram_total_gb']} GB)\n"
            f"Disk / {s['disk_root_percent']}% | Uptime {human_duration(s['uptime_s'])}"
        )
