from __future__ import annotations

from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from neonctl.backend.repositories import RepositoryService


class RepositoriesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = RepositoryService()

        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        top.addWidget(QLabel("<h2>Repositories</h2>"))
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.reload)
        self.sync_btn = QPushButton("Sync metadata (root)")
        self.sync_btn.clicked.connect(self.sync_metadata)
        top.addWidget(self.refresh_btn)
        top.addWidget(self.sync_btn)
        top.addStretch()
        lay.addLayout(top)

        form_w = QWidget()
        self.form = QFormLayout(form_w)
        self.supported_lbl = QLabel()
        self.manager_lbl = QLabel()
        self.form.addRow("Supported:", self.supported_lbl)
        self.form.addRow("Manager:", self.manager_lbl)
        lay.addWidget(form_w)

        self.listing = QListWidget()
        lay.addWidget(self.listing)

        self.reload()

    def reload(self):
        data = self.service.status()
        self.supported_lbl.setText("Yes" if data.get("supported") else "No")
        self.manager_lbl.setText(str(data.get("manager", "none")))
        repos = self.service.list_repos()
        self.listing.clear()
        if not repos:
            self.listing.addItem("No repositories detected.")
            return
        for repo in repos:
            self.listing.addItem(repo)

    def sync_metadata(self):
        res = self.service.refresh_metadata()
        if res is None:
            QMessageBox.information(self, "Repositories", "No supported repository tool found.")
            return
        if res.returncode == 0:
            QMessageBox.information(self, "Repositories", "Repository metadata synced.")
        else:
            QMessageBox.warning(
                self,
                "Repositories",
                (res.stderr or res.stdout or "Failed to sync repositories.").strip(),
            )
        self.reload()
