from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from neonctl.backend.disks import DiskService


class DisksPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = DiskService()

        layout = QVBoxLayout(self)

        header = QHBoxLayout()
        title = QLabel("<h2>Disks</h2>")
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.refresh_btn)
        layout.addLayout(header)

        self.summary_group = QGroupBox("Usage Summary")
        self.summary_layout = QGridLayout(self.summary_group)
        layout.addWidget(self.summary_group)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Device", "Mount Point", "Filesystem", "Used %"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.refresh()

    def refresh(self):
        data = self.service.status()
        mounts = data.get("mounts", []) if isinstance(data, dict) else []

        while self.summary_layout.count():
            item = self.summary_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        if not mounts:
            self.summary_layout.addWidget(QLabel("No disk data available."), 0, 0)
            self.table.setRowCount(0)
            return

        self.table.setRowCount(len(mounts))
        for i, m in enumerate(mounts):
            used = float(m.get("used_percent", 0.0))
            self.table.setItem(i, 0, QTableWidgetItem(m.get("device", "?")))
            self.table.setItem(i, 1, QTableWidgetItem(m.get("mountpoint", "?")))
            self.table.setItem(i, 2, QTableWidgetItem(m.get("fstype", "?")))
            self.table.setItem(i, 3, QTableWidgetItem(f"{used:.1f}%"))

            card = QGroupBox(m.get("mountpoint", "disk"))
            card_l = QVBoxLayout(card)
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(int(used))
            bar.setFormat(f"{used:.1f}% used")
            bar.setAlignment(Qt.AlignCenter)
            chunk_color = "#00e676"
            if used >= 90:
                chunk_color = "#ff1744"
            elif used >= 75:
                chunk_color = "#ffab00"
            bar.setStyleSheet(
                "QProgressBar {"
                "border: 1px solid #a35a00;"
                "background: #120700;"
                "color: #ffe0a8;"
                "}"
                "QProgressBar::chunk {"
                f"background-color: {chunk_color};"
                "}"
            )
            card_l.addWidget(QLabel(f"Device: {m.get('device', '?')}"))
            card_l.addWidget(QLabel(f"FS: {m.get('fstype', '?')}"))
            card_l.addWidget(bar)

            self.summary_layout.addWidget(card, i // 2, i % 2, alignment=Qt.AlignTop)
