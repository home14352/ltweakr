from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from neonctl.backend.processes import ProcessesService


class ProcessesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = ProcessesService()
        self.rows: list[dict[str, str]] = []

        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.reload)
        self.kill_btn = QPushButton("Terminate Selected")
        self.kill_btn.clicked.connect(self.kill_selected)
        self.clean_ram_btn = QPushButton("Clean RAM (drop caches)")
        self.clean_ram_btn.clicked.connect(self.clean_ram)
        self.live_btn = QPushButton("Start live")
        self.live_btn.clicked.connect(self.toggle_live)
        self.save_btn = QPushButton("Save snapshot")
        self.save_btn.clicked.connect(self.save_snapshot)
        top.addWidget(self.refresh_btn)
        top.addWidget(self.kill_btn)
        top.addWidget(self.clean_ram_btn)
        top.addWidget(self.live_btn)
        top.addWidget(self.save_btn)
        top.addStretch()
        lay.addLayout(top)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["PID", "Name", "User", "CPU%", "MEM%"])
        lay.addWidget(self.table)

        self.timer = QTimer(self)
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.reload)
        self.reload()

    def reload(self):
        self.rows = self.service.list_processes(limit=400)
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(self.rows))
        for i, row in enumerate(self.rows):
            self.table.setItem(i, 0, QTableWidgetItem(row["pid"]))
            self.table.setItem(i, 1, QTableWidgetItem(row["name"]))
            self.table.setItem(i, 2, QTableWidgetItem(row["user"]))
            self.table.setItem(i, 3, QTableWidgetItem(row["cpu"]))
            self.table.setItem(i, 4, QTableWidgetItem(row["mem"]))
        self.table.setSortingEnabled(True)

    def selected_pid(self) -> int | None:
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        if item is None:
            return None
        try:
            return int(item.text())
        except ValueError:
            return None

    def kill_selected(self):
        pid = self.selected_pid()
        if pid is None:
            QMessageBox.information(self, "Process manager", "Select a process first.")
            return
        if (
            QMessageBox.question(self, "Confirm terminate", f"Terminate process {pid}?")
            != QMessageBox.StandardButton.Yes
        ):
            return
        ok = self.service.terminate(pid)
        QMessageBox.information(self, "Process manager", "Process terminated." if ok else "Failed.")
        self.reload()

    def clean_ram(self):
        if (
            QMessageBox.question(
                self,
                "Confirm RAM cleaner",
                "Run RAM cleaner (sync + drop caches)? This requires root.",
            )
            != QMessageBox.StandardButton.Yes
        ):
            return
        ok = self.service.clean_ram()
        QMessageBox.information(self, "RAM cleaner", "Completed." if ok else "Failed.")

    def toggle_live(self):
        if self.timer.isActive():
            self.timer.stop()
            self.live_btn.setText("Start live")
        else:
            self.timer.start()
            self.live_btn.setText("Stop live")

    def save_snapshot(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save process snapshot", "neonctl_processes.csv", "CSV Files (*.csv)"
        )
        if not path:
            return
        lines = ["pid,name,user,cpu,mem"]
        for row in self.rows:
            lines.append(",".join([row["pid"], row["name"], row["user"], row["cpu"], row["mem"]]))
        Path(path).write_text("\n".join(lines))
