from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from neonctl.backend.security import SecurityService


class SecurityPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = SecurityService()
        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        top.addWidget(QLabel("<h2>Security</h2>"))
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.reload)
        top.addWidget(self.refresh_btn)
        top.addStretch()
        lay.addLayout(top)

        form_w = QWidget()
        self.form = QFormLayout(form_w)
        self.selinux = QLabel("-")
        self.apparmor = QLabel("-")
        self.firewall = QLabel("-")
        self.form.addRow("SELinux:", self.selinux)
        self.form.addRow("AppArmor:", self.apparmor)
        self.form.addRow("Firewall:", self.firewall)
        lay.addWidget(form_w)
        self.tips = QLabel()
        self.tips.setWordWrap(True)
        lay.addWidget(self.tips)
        lay.addStretch()
        self.reload()

    def reload(self):
        data = self.service.status()
        self.selinux.setText(str(data.get("selinux", "unknown")))
        self.apparmor.setText(str(data.get("apparmor", "unknown")))
        self.firewall.setText(str(data.get("firewall", "unknown")))
        self.tips.setText(
            "Tip: keep firewall enabled, apply updates regularly, and only run trusted elevation prompts."
        )
