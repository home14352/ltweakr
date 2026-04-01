from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from neonctl.backend.history import append_history
from neonctl.backend.packages import PackageService
from neonctl.ui.installed_packages_tab import InstalledPackagesTab


class PackagePage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = PackageService()

        lay = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.addTab(InstalledPackagesTab(), "Installed Packages")
        tabs.addTab(self._build_manager_tab(), "Application Manager")
        lay.addWidget(tabs)

    def _build_manager_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)

        self.manager_label = QLabel(
            f"Active native manager: {self.service.manager_name or 'not detected'}"
        )
        lay.addWidget(self.manager_label)

        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search available packages")
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self._search)
        search_row.addWidget(self.search_input)
        search_row.addWidget(self.search_btn)
        lay.addLayout(search_row)

        action_row = QHBoxLayout()
        self.pkg_input = QLineEdit()
        self.pkg_input.setPlaceholderText("Package name (install/remove)")
        self.install_btn = QPushButton("Install")
        self.remove_btn = QPushButton("Remove")
        self.install_btn.clicked.connect(self._install)
        self.remove_btn.clicked.connect(self._remove)
        action_row.addWidget(self.pkg_input)
        action_row.addWidget(self.install_btn)
        action_row.addWidget(self.remove_btn)
        lay.addLayout(action_row)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        lay.addWidget(self.output)

        return w

    def _append_result(self, title: str, result) -> None:
        append_history(
            command=" ".join(result.command),
            success=result.returncode == 0,
            summary=title,
        )
        self.output.append(f"\n=== {title} ===")
        self.output.append(f"Command: {' '.join(result.command)}")
        self.output.append(f"Exit code: {result.returncode}")
        if result.stdout.strip():
            self.output.append(result.stdout.strip())
        if result.stderr.strip():
            self.output.append(f"ERR: {result.stderr.strip()}")

    def _search(self) -> None:
        query = self.search_input.text().strip()
        if not query:
            return
        res = self.service.search(query)
        self._append_result(f"Search '{query}'", res)

    def _install(self) -> None:
        name = self.pkg_input.text().strip()
        if not name:
            return
        if (
            QMessageBox.question(
                self,
                "Confirm install",
                f"Install package '{name}' with elevated privileges?",
            )
            != QMessageBox.StandardButton.Yes
        ):
            return
        res = self.service.install(name, elevated=True)
        self._append_result(f"Install '{name}'", res)

    def _remove(self) -> None:
        name = self.pkg_input.text().strip()
        if not name:
            return
        if (
            QMessageBox.question(
                self,
                "Confirm removal",
                f"Remove package '{name}' with elevated privileges?",
            )
            != QMessageBox.StandardButton.Yes
        ):
            return
        res = self.service.remove(name, elevated=True)
        self._append_result(f"Remove '{name}'", res)
