import json

from PySide6.QtWidgets import QHBoxLayout, QPushButton, QTextEdit, QVBoxLayout, QWidget

from neonctl.backend.updates import UpdateService


class UpdatesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = UpdateService()
        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh updates")
        self.refresh_btn.clicked.connect(self.reload)
        top.addWidget(self.refresh_btn)
        top.addStretch()
        lay.addLayout(top)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        lay.addWidget(self.output)
        self.reload()

    def reload(self):
        updates = self.service.list_updates()
        payload = {"count": len(updates), "updates": updates[:300]}
        self.output.setPlainText(json.dumps(payload, indent=2))
