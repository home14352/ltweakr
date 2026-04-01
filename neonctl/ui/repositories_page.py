from __future__ import annotations

from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
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

        edit_row = QHBoxLayout()
        self.repo_input = QLineEdit()
        self.repo_input.setPlaceholderText("Repo URL or repo id (manager-specific)")
        self.add_btn = QPushButton("Add repo")
        self.add_btn.clicked.connect(self.add_repo)
        self.remove_btn = QPushButton("Disable/remove repo")
        self.remove_btn.clicked.connect(self.remove_repo)
        edit_row.addWidget(self.repo_input)
        edit_row.addWidget(self.add_btn)
        edit_row.addWidget(self.remove_btn)
        lay.addLayout(edit_row)

        self.reload()

    def add_repo(self):
        value = self.repo_input.text().strip()
        if not value:
            return
        res = self.service.add_repo(value)
        if res is None:
            QMessageBox.information(self, "Repositories", "Add repo is unsupported for this manager.")
            return
        if res.returncode == 0:
            QMessageBox.information(self, "Repositories", "Repository added.")
        else:
            QMessageBox.warning(self, "Repositories", (res.stderr or res.stdout or "Failed.").strip())
        self.reload()

    def remove_repo(self):
        value = self.repo_input.text().strip()
        if not value:
            return
        res = self.service.remove_repo(value)
        if res is None:
            QMessageBox.information(
                self, "Repositories", "Disable/remove repo is unsupported for this manager."
            )
            return
        if res.returncode == 0:
            QMessageBox.information(self, "Repositories", "Repository updated.")
        else:
            QMessageBox.warning(self, "Repositories", (res.stderr or res.stdout or "Failed.").strip())
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
