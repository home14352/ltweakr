from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from neonctl.backend.appimage import AppImageService


class AppimagePage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = AppImageService()
        self.files: list[Path] = []

        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        self.scan_btn = QPushButton("Scan")
        self.exec_btn = QPushButton("Make Executable")
        self.launch_btn = QPushButton("Launch")
        self.scan_btn.clicked.connect(self.scan)
        self.exec_btn.clicked.connect(self.make_exec)
        self.launch_btn.clicked.connect(self.launch)
        top.addWidget(self.scan_btn)
        top.addWidget(self.exec_btn)
        top.addWidget(self.launch_btn)
        top.addStretch()
        lay.addLayout(top)

        self.listing = QListWidget()
        lay.addWidget(self.listing)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        lay.addWidget(self.output)
        self.scan()

    def scan(self):
        self.files = self.service.list_appimages()
        self.listing.clear()
        for p in self.files:
            self.listing.addItem(str(p))
        self.output.setPlainText(f"Found {len(self.files)} AppImage files.")

    def selected(self) -> Path | None:
        row = self.listing.currentRow()
        if row < 0 or row >= len(self.files):
            return None
        return self.files[row]

    def make_exec(self):
        p = self.selected()
        if not p:
            return
        ok = self.service.make_executable(p)
        state = "set" if ok else "failed"
        QMessageBox.information(self, "AppImage", f"Executable flag {state} for {p.name}")

    def launch(self):
        p = self.selected()
        if not p:
            return
        if (
            QMessageBox.question(self, "Launch", f"Launch {p.name}?")
            != QMessageBox.StandardButton.Yes
        ):
            return
        res = self.service.launch(p)
        self.output.append(f"Launch rc={res.returncode}")
        if res.stdout.strip():
            self.output.append(res.stdout.strip())
        if res.stderr.strip():
            self.output.append(res.stderr.strip())
