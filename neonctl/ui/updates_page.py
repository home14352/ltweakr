from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
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
        top.addWidget(self.refresh_btn)
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
