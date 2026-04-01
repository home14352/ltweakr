from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from neonctl.backend.history import read_history


class TasksPage(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)

        controls = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh History")
        self.refresh_btn.clicked.connect(self.reload)
        controls.addWidget(self.refresh_btn)
        controls.addStretch()
        lay.addLayout(controls)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["When (UTC)", "Status", "Command", "Summary"])
        lay.addWidget(self.table)
        self.reload()

    def reload(self):
        rows = read_history(limit=300)
        self.table.setRowCount(len(rows))
        for i, item in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(item.when.isoformat()))
            self.table.setItem(i, 1, QTableWidgetItem("OK" if item.success else "FAIL"))
            self.table.setItem(i, 2, QTableWidgetItem(item.command))
            self.table.setItem(i, 3, QTableWidgetItem(item.summary))
