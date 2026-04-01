from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from neonctl.backend.monitoring import collect_stats
from neonctl.utils.formatters import human_duration


class NeonTray:
    def __init__(self, icon, parent, open_page_cb, settings, quit_cb):
        tray_icon = icon if isinstance(icon, QIcon) else QIcon()
        self.tray = QSystemTrayIcon(tray_icon, parent)
        self.menu = QMenu()

        title_action = QAction("NeonCtl Control Tray", parent)
        title_action.setEnabled(False)
        self.menu.addAction(title_action)
        self.menu.addSeparator()

        self.menu.addAction(QAction("Show Window", parent, triggered=parent.showNormal))
        self.menu.addAction(
            QAction("Open Dashboard", parent, triggered=lambda: open_page_cb("Dashboard"))
        )
        self.menu.addAction(
            QAction("Open Packages", parent, triggered=lambda: open_page_cb("Packages"))
        )
        self.menu.addAction(
            QAction("Open Updates", parent, triggered=lambda: open_page_cb("Updates"))
        )
        self.menu.addAction(
            QAction("Open Diagnostics", parent, triggered=lambda: open_page_cb("Diagnostics"))
        )

        self.menu.addSeparator()
        self.menu.addAction(QAction("Refresh Stats", parent, triggered=self.refresh_tooltip))
        self.menu.addSeparator()
        self.menu.addAction(QAction("Quit NeonCtl", parent, triggered=quit_cb))
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
            "NeonCtl\n"
            f"🧠 CPU: {s['cpu_percent']}%\n"
            f"🧮 RAM: {s['ram_percent']}% ({s['ram_used_gb']}/{s['ram_total_gb']} GB)\n"
            f"💽 Disk /: {s['disk_root_percent']}%\n"
            f"⏱ Uptime: {human_duration(s['uptime_s'])}"
        )

    def shutdown(self):
        self.timer.stop()
        self.tray.hide()
        QApplication.instance().processEvents()
