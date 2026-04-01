from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget

from neonctl.backend.users import UsersService


class UsersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = UsersService()

        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        top.addWidget(QLabel("<h2>Users</h2>"))
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.reload)
        top.addWidget(self.refresh_btn)
        top.addStretch()
        lay.addLayout(top)

        form_w = QWidget()
        form = QFormLayout(form_w)
        self.user_lbl = QLabel("-")
        self.count_lbl = QLabel("-")
        form.addRow("Current user:", self.user_lbl)
        form.addRow("Group count:", self.count_lbl)
        lay.addWidget(form_w)

        self.groups = QListWidget()
        lay.addWidget(self.groups)
        self.reload()

    def reload(self):
        data = self.service.status()
        self.user_lbl.setText(str(data.get("current_user", "-")))
        self.count_lbl.setText(str(data.get("group_count", 0)))
        self.groups.clear()
        for group in data.get("groups", []):
            self.groups.addItem(group)
