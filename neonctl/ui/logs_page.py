from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from neonctl.backend.logs import LogsService


class LogsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = LogsService()

        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        top.addWidget(QLabel("<h2>Logs</h2>"))
        top.addWidget(QLabel("Lines:"))
        self.lines = QSpinBox()
        self.lines.setRange(20, 2000)
        self.lines.setValue(250)
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.reload)
        top.addWidget(self.lines)
        top.addWidget(self.refresh_btn)
        top.addStretch()
        lay.addLayout(top)

        self.summary = QLabel()
        lay.addWidget(self.summary)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        lay.addWidget(self.output)

        self.reload()

    def reload(self):
        data = self.service.status()
        self.summary.setText(
            f"Source: <b>{data.get('source', 'unknown')}</b> | "
            f"Supported: <b>{'Yes' if data.get('supported') else 'No'}</b>"
        )
        self.output.setPlainText(self.service.recent(self.lines.value()))
