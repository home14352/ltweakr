import json

from PySide6.QtWidgets import QHBoxLayout, QPushButton, QTextEdit, QVBoxLayout, QWidget

from neonctl.backend.repositories import RepositoryService


class RepositoriesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = RepositoryService()
        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.reload)
        top.addWidget(self.refresh_btn)
        top.addStretch()
        lay.addLayout(top)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        lay.addWidget(self.output)
        self.reload()

    def reload(self):
        data = self.service.status()
        data["repositories"] = self.service.list_repos()
        self.output.setPlainText(json.dumps(data, indent=2, ensure_ascii=False))
