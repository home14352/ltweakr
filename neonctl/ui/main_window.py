from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QStackedWidget,
    QWidget,
)

from neonctl.backend.config import ConfigManager
from neonctl.backend.themes import theme_path
from neonctl.ui.about_page import AboutPage
from neonctl.ui.appimage_page import AppimagePage
from neonctl.ui.backups_page import BackupsPage
from neonctl.ui.cleanup_page import CleanupPage
from neonctl.ui.containers_page import ContainersPage
from neonctl.ui.dashboard_page import DashboardPage
from neonctl.ui.diagnostics_page import DiagnosticsPage
from neonctl.ui.disks_page import DisksPage
from neonctl.ui.flatpak_page import FlatpakPage
from neonctl.ui.logs_page import LogsPage
from neonctl.ui.navigation import PAGES
from neonctl.ui.network_page import NetworkPage
from neonctl.ui.package_page import PackagePage
from neonctl.ui.processes_page import ProcessesPage
from neonctl.ui.repositories_page import RepositoriesPage
from neonctl.ui.security_page import SecurityPage
from neonctl.ui.services_page import ServicesPage
from neonctl.ui.settings_page import SettingsPage
from neonctl.ui.snap_page import SnapPage
from neonctl.ui.tasks_page import TasksPage
from neonctl.ui.tray import NeonTray
from neonctl.ui.tweaks_page import TweaksPage
from neonctl.ui.updates_page import UpdatesPage
from neonctl.ui.users_page import UsersPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeonCtl")
        self.resize(1280, 840)
        self._allow_quit = False
        self.config = ConfigManager()
        self.settings = self.config.load()

        central = QWidget()
        self.setCentralWidget(central)
        lay = QHBoxLayout(central)

        self.nav = QListWidget()
        for name in PAGES:
            QListWidgetItem(name, self.nav)
        self.stack = QStackedWidget()
        lay.addWidget(self.nav, 1)
        lay.addWidget(self.stack, 5)

        self.page_map = {
            "Dashboard": DashboardPage(),
            "Packages": PackagePage(),
            "Updates": UpdatesPage(),
            "Repositories": RepositoriesPage(),
            "Flatpak": FlatpakPage(),
            "Snap": SnapPage(),
            "AppImage": AppimagePage(),
            "Services": ServicesPage(),
            "Logs": LogsPage(),
            "Processes": ProcessesPage(),
            "Tweaks": TweaksPage(),
            "Network": NetworkPage(),
            "Disks": DisksPage(),
            "Users": UsersPage(),
            "Security": SecurityPage(),
            "Cleanup": CleanupPage(),
            "Containers": ContainersPage(),
            "Backups": BackupsPage(),
            "Tasks": TasksPage(),
            "Diagnostics": DiagnosticsPage(),
            "Settings": SettingsPage(self._settings_saved),
            "About": AboutPage(),
        }
        for name in PAGES:
            self.stack.addWidget(self.page_map[name])
        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav.setCurrentRow(0)

        qss_path = theme_path(self.settings.theme)
        if qss_path.exists():
            self.setStyleSheet(qss_path.read_text())

        self.tray = None
        if QIcon.hasThemeIcon("applications-system"):
            icon = QIcon.fromTheme("applications-system")
        else:
            icon = self.windowIcon()
        if self.settings.close_to_tray:
            from PySide6.QtWidgets import QSystemTrayIcon

            if QSystemTrayIcon.isSystemTrayAvailable():
                self.tray = NeonTray(
                    icon, self, self.open_page, self.settings, self.quit_application
                )
                self.tray.show()

    def _settings_saved(self, settings):
        self.settings = settings

    def open_page(self, name: str):
        idx = PAGES.index(name)
        self.nav.setCurrentRow(idx)
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event):
        if self.settings.close_to_tray and self.tray and not self._allow_quit:
            event.ignore()
            self.hide()
            return
        super().closeEvent(event)

    def force_quit(self):
        self.quit_application()

    def quit_application(self):
        self._allow_quit = True
        if self.tray:
            self.tray.shutdown()
        self.close()
