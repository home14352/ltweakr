from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

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
        row = QHBoxLayout()
        self.engine = QComboBox()
        self.refresh_ct_btn = QPushButton("List containers")
        self.refresh_ct_btn.clicked.connect(self.reload_containers)
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(lambda: self.run_action("start"))
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(lambda: self.run_action("stop"))
        self.remove_btn = QPushButton("Remove")
        self.remove_btn.clicked.connect(lambda: self.run_action("rm"))
        row.addWidget(self.engine)
        row.addWidget(self.refresh_ct_btn)
        row.addWidget(self.start_btn)
        row.addWidget(self.stop_btn)
        row.addWidget(self.remove_btn)
        row.addStretch()
        lay.addLayout(row)
        self.containers = QListWidget()
        lay.addWidget(self.containers)
        self.reload()

    def reload(self):
        data = self.service.status()
        self.summary.setText(f"Available tools: <b>{data.get('available_count', 0)}</b>")
        self.tools.clear()
        self.engine.clear()
        for name, enabled in (data.get("tools") or {}).items():
            self.tools.addItem(f"{name}: {'installed' if enabled else 'not found'}")
            self.engine.addItem(name)
            idx = self.engine.count() - 1
            if not enabled:
                self.engine.setItemData(idx, QColor("#777777"), role=Qt.ItemDataRole.ForegroundRole)
        self.reload_containers()

    def reload_containers(self):
        engine = self.engine.currentText()
        rows = self.service.list_containers(engine)
        self.containers.clear()
        for row in rows:
            self.containers.addItem(row)

    def run_action(self, action: str):
        item = self.containers.currentItem()
        if item is None:
            return
        name = item.text().split("\t", 1)[0]
        res = self.service.run_action(self.engine.currentText(), action, name)
        if res is None:
            QMessageBox.information(self, "Containers", "Engine unavailable.")
            return
        QMessageBox.information(self, "Containers", f"Exit code: {res.returncode}")
        self.reload_containers()
