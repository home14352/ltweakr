from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget

from neonctl.backend.backups import BackupsService


class BackupsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = BackupsService()
        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        top.addWidget(QLabel("<h2>Backups</h2>"))
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.reload)
        top.addWidget(self.refresh_btn)
        top.addStretch()
        lay.addLayout(top)

        info = QWidget()
        form = QFormLayout(info)
        self.path_lbl = QLabel("-")
        self.count_lbl = QLabel("0")
        form.addRow("Backup folder:", self.path_lbl)
        form.addRow("Backups found:", self.count_lbl)
        lay.addWidget(info)

        self.items = QListWidget()
        lay.addWidget(self.items)
        self.reload()

    def reload(self):
        data = self.service.status()
        self.path_lbl.setText(str(data.get("backup_dir", "-")))
        self.count_lbl.setText(str(data.get("backup_count", 0)))
        self.items.clear()
        for item in data.get("backups", []):
            self.items.addItem(item)
