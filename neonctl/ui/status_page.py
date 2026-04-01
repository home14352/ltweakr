from __future__ import annotations

import json

from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget


class StatusPage(QWidget):
    def __init__(self, title: str, provider):
        super().__init__()
        self.title = title
        self.provider = provider

        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        top.addWidget(QLabel(f"<h2>{title}</h2>"))
        top.addStretch()
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        top.addWidget(self.refresh_btn)
        lay.addLayout(top)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        lay.addWidget(self.output)

        self.refresh()

    def refresh(self):
        try:
            data = self.provider.status()
            self.output.setPlainText(json.dumps(data, indent=2, ensure_ascii=False))
        except Exception as exc:  # noqa: BLE001
            self.output.setPlainText(f"Failed to load {self.title} status: {exc}")
