from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from neonctl.backend.inventory import InventoryService
from neonctl.backend.workers import Worker


class InstalledPackagesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.inventory = InventoryService()
        self.pool = QThreadPool.globalInstance()
        self.records = []

        lay = QVBoxLayout(self)
        controls = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Filter installed packages")
        self.search.textChanged.connect(self.render)
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load)
        self.export_btn = QPushButton("Export CSV")
        self.export_btn.clicked.connect(self.export_csv)
        controls.addWidget(self.search)
        controls.addWidget(self.refresh_btn)
        controls.addWidget(self.export_btn)
        lay.addLayout(controls)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Name", "Version", "Arch"])
        lay.addWidget(self.table)
        self.load()

    def load(self):
        self.refresh_btn.setEnabled(False)
        w = Worker(self.inventory.all_installed)
        w.signals.finished.connect(self._loaded)
        w.signals.error.connect(lambda e: self.refresh_btn.setEnabled(True))
        self.pool.start(w)

    def _loaded(self, records):
        self.records = records
        self.refresh_btn.setEnabled(True)
        self.render()

    def render(self):
        q = self.search.text().lower().strip()
        data = [r for r in self.records if q in r.name.lower()] if q else self.records
        self.table.setRowCount(len(data))
        for row, r in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(r.name))
            self.table.setItem(row, 1, QTableWidgetItem(r.version))
            self.table.setItem(row, 2, QTableWidgetItem(r.arch))

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export package inventory", "packages.csv", "CSV (*.csv)"
        )
        if not path:
            return
        from pathlib import Path

        self.inventory.export_csv(self.records, Path(path))
