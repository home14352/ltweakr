from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from neonctl.backend.diagnostics import run_checks
from neonctl.backend.report import diagnostics_report


class DiagnosticsPage(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)

        row = QHBoxLayout()
        self.refresh_btn = QPushButton("Run Checks")
        self.refresh_btn.clicked.connect(self.reload)
        self.export_btn = QPushButton("Export Report")
        self.export_btn.clicked.connect(self.export_report)
        row.addWidget(self.refresh_btn)
        row.addWidget(self.export_btn)
        row.addStretch()
        lay.addLayout(row)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Check", "Status", "Detail"])
        lay.addWidget(self.table)

        self.reload()

    def reload(self):
        results = run_checks()
        self.table.setRowCount(len(results))
        for idx, item in enumerate(results):
            self.table.setItem(idx, 0, QTableWidgetItem(item.get("name", "unknown")))
            self.table.setItem(idx, 1, QTableWidgetItem("OK" if item.get("ok") else "WARN"))
            self.table.setItem(idx, 2, QTableWidgetItem(item.get("detail", "")))

    def export_report(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export diagnostics report",
            "neonctl_diagnostics.txt",
            "Text Files (*.txt)",
        )
        if not path:
            return
        Path(path).write_text(diagnostics_report())
