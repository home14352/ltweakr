from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from neonctl.ui.base_page import SimplePage
from neonctl.ui.installed_packages_tab import InstalledPackagesTab


class PackagePage(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.addTab(InstalledPackagesTab(), "Installed Packages")
        tabs.addTab(
            SimplePage(
                "Search Available Packages", "Native repository search mode is manager-dependent."
            ),
            "Available Search",
        )
        lay.addWidget(tabs)
