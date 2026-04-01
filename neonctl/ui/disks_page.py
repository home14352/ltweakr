from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
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


class InvertedTextProgressBar(QProgressBar):
    """Progress bar with text that inverts color over the filled chunk."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._chunk_color = QColor("#00e676")
        self._bg_color = QColor("#120700")
        self._border_color = QColor("#a35a00")
        self._text_on_bg = QColor("#ffe0a8")
        self._text_on_chunk = QColor("#101010")

    def set_chunk_color(self, color: str) -> None:
        self._chunk_color = QColor(color)
        self.update()

    def paintEvent(self, event):  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        rect = self.rect().adjusted(0, 0, -1, -1)
        radius = 3

        painter.setPen(self._border_color)
        painter.setBrush(self._bg_color)
        painter.drawRoundedRect(rect, radius, radius)

        progress = 0.0
        if self.maximum() > self.minimum():
            progress = (self.value() - self.minimum()) / (self.maximum() - self.minimum())
        fill_w = max(0, int(rect.width() * progress))
        fill_rect = rect.adjusted(1, 1, -(rect.width() - fill_w), -1)
        if fill_rect.width() > 0:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(self._chunk_color)
            painter.drawRect(fill_rect)

        text = self.text()
        if not text:
            return

        painter.setPen(self._text_on_bg)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

        if fill_rect.width() > 0:
            painter.save()
            painter.setClipRect(fill_rect)
            painter.setPen(self._text_on_chunk)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
            painter.restore()


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
            bar = InvertedTextProgressBar()
            bar.setRange(0, 100)
            bar.setValue(int(used))
            bar.setFormat(f"{used:.1f}% used")
            chunk_color = "#00e676"
            if used >= 90:
                chunk_color = "#ff1744"
            elif used >= 75:
                chunk_color = "#ffab00"
            bar.set_chunk_color(chunk_color)
            card_l.addWidget(QLabel(f"Device: {m.get('device', '?')}"))
            card_l.addWidget(QLabel(f"FS: {m.get('fstype', '?')}"))
            card_l.addWidget(bar)

            self.summary_layout.addWidget(card, i // 2, i % 2, alignment=Qt.AlignTop)
