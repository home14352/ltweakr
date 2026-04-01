from __future__ import annotations

from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget

from neonctl.backend.cleanup import CleanupService


class CleanupPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = CleanupService()
        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        top.addWidget(QLabel("<h2>Cleanup</h2>"))
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.reload)
        self.copy_btn = QPushButton("Copy selected command")
        self.copy_btn.clicked.connect(self.copy_selected)
        top.addWidget(self.refresh_btn)
        top.addWidget(self.copy_btn)
        top.addStretch()
        lay.addLayout(top)

        self.summary = QLabel()
        lay.addWidget(self.summary)
        self.listing = QListWidget()
        lay.addWidget(self.listing)
        self.reload()

    def reload(self):
        data = self.service.status()
        self.summary.setText(f"Package manager: <b>{data.get('manager', 'none')}</b>")
        self.listing.clear()
        for cmd in data.get("recommendations", []):
            self.listing.addItem(cmd)

    def copy_selected(self):
        item = self.listing.currentItem()
        if item is None:
            return
        QGuiApplication.clipboard().setText(item.text())
