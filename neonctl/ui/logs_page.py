from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QFileDialog,
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
        self.live_btn = QPushButton("Start live")
        self.live_btn.clicked.connect(self.toggle_live)
        self.save_btn = QPushButton("Save log snapshot")
        self.save_btn.clicked.connect(self.save_snapshot)
        top.addWidget(self.lines)
        top.addWidget(self.refresh_btn)
        top.addWidget(self.live_btn)
        top.addWidget(self.save_btn)
        top.addStretch()
        lay.addLayout(top)

        self.summary = QLabel()
        lay.addWidget(self.summary)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        lay.addWidget(self.output)

        self.timer = QTimer(self)
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.reload)

        self.reload()

    def reload(self):
        data = self.service.status()
        self.summary.setText(
            f"Source: <b>{data.get('source', 'unknown')}</b> | "
            f"Supported: <b>{'Yes' if data.get('supported') else 'No'}</b>"
        )
        self.output.setPlainText(self.service.recent(self.lines.value()))

    def toggle_live(self):
        if self.timer.isActive():
            self.timer.stop()
            self.live_btn.setText("Start live")
        else:
            self.timer.start()
            self.live_btn.setText("Stop live")

    def save_snapshot(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save logs", "neonctl_logs.txt", "Text Files (*.txt)")
        if not path:
            return
        Path(path).write_text(self.output.toPlainText())
