from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from neonctl.backend.updates import UpdateService


class UpdatesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = UpdateService()

        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        top.addWidget(QLabel("<h2>Updates</h2>"))
        self.refresh_btn = QPushButton("Refresh updates")
        self.refresh_btn.clicked.connect(self.reload)
        self.refresh_index_btn = QPushButton("Sync metadata (root)")
        self.refresh_index_btn.clicked.connect(self.refresh_metadata)
        top.addWidget(self.refresh_btn)
        top.addWidget(self.refresh_index_btn)
        top.addStretch()
        lay.addLayout(top)

        self.summary = QLabel()
        lay.addWidget(self.summary)

        self.listing = QListWidget()
        lay.addWidget(self.listing)

        self.reload()

    def reload(self):
        updates = self.service.list_updates()
        self.summary.setText(f"Pending updates: <b>{len(updates)}</b>")
        self.listing.clear()
        if not updates:
            self.listing.addItem("No updates found.")
            return
        for line in updates[:500]:
            self.listing.addItem(line)

    def refresh_metadata(self):
        res = self.service.refresh_metadata()
        if res is None:
            QMessageBox.information(self, "Updates", "No supported package manager found.")
            return
        if res.returncode == 0:
            QMessageBox.information(self, "Updates", "Metadata refreshed successfully.")
        else:
            QMessageBox.warning(
                self,
                "Updates",
                (res.stderr or res.stdout or "Failed to refresh package metadata.").strip(),
            )
        self.reload()
