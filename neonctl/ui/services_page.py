from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from neonctl.backend.services import ServicesService


class ServicesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = ServicesService()
        self.rows: list[dict[str, str]] = []

        lay = QVBoxLayout(self)

        top = QHBoxLayout()
        self.filter = QComboBox()
        self.filter.addItems(["all", "running", "failed"])
        self.filter.currentTextChanged.connect(self.reload)
        self.reload_btn = QPushButton("Refresh")
        self.reload_btn.clicked.connect(self.reload)
        top.addWidget(self.filter)
        top.addWidget(self.reload_btn)
        top.addStretch()
        lay.addLayout(top)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Unit", "Load", "Active", "Sub", "Description"])
        lay.addWidget(self.table)

        actions = QHBoxLayout()
        for action in ["start", "stop", "restart", "enable", "disable"]:
            btn = QPushButton(action.capitalize())
            btn.clicked.connect(lambda _=False, a=action: self.do_action(a))
            actions.addWidget(btn)
        actions.addStretch()
        lay.addLayout(actions)

        self.reload()

    def reload(self):
        mode = self.filter.currentText()
        state = None if mode == "all" else mode
        self.rows = self.service.list_services(state=state)
        self.table.setRowCount(len(self.rows))
        for i, row in enumerate(self.rows):
            self.table.setItem(i, 0, QTableWidgetItem(row["unit"]))
            self.table.setItem(i, 1, QTableWidgetItem(row["load"]))
            self.table.setItem(i, 2, QTableWidgetItem(row["active"]))
            self.table.setItem(i, 3, QTableWidgetItem(row["sub"]))
            self.table.setItem(i, 4, QTableWidgetItem(row["description"]))

    def selected_unit(self) -> str | None:
        row = self.table.currentRow()
        if row < 0 or row >= len(self.rows):
            return None
        return self.rows[row]["unit"]

    def do_action(self, action: str):
        unit = self.selected_unit()
        if not unit:
            QMessageBox.information(self, "Service action", "Select a service first.")
            return
        if (
            QMessageBox.question(
                self,
                "Confirm service action",
                f"Run '{action}' on {unit}?",
            )
            != QMessageBox.StandardButton.Yes
        ):
            return
        ok = self.service.manage(action, unit)
        QMessageBox.information(
            self,
            "Service action",
            f"{action} on {unit} {'succeeded' if ok else 'failed'}.",
        )
        self.reload()
