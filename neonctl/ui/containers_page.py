from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget

from neonctl.backend.containers import ContainersService


class ContainersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = ContainersService()
        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        top.addWidget(QLabel("<h2>Containers</h2>"))
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.reload)
        top.addWidget(self.refresh_btn)
        top.addStretch()
        lay.addLayout(top)

        self.summary = QLabel()
        lay.addWidget(self.summary)
        self.tools = QListWidget()
        lay.addWidget(self.tools)
        self.reload()

    def reload(self):
        data = self.service.status()
        self.summary.setText(f"Available tools: <b>{data.get('available_count', 0)}</b>")
        self.tools.clear()
        for name, enabled in (data.get("tools") or {}).items():
            self.tools.addItem(f"{name}: {'installed' if enabled else 'not found'}")
