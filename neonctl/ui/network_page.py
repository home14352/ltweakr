from __future__ import annotations

from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from neonctl.backend.network import NetworkService


class NetworkPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = NetworkService()

        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        top.addWidget(QLabel("<h2>Network</h2>"))
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.reload)
        top.addWidget(self.refresh_btn)
        top.addStretch()
        lay.addLayout(top)

        self.route_card = QGroupBox("Default route")
        route_l = QVBoxLayout(self.route_card)
        self.route_text = QLabel("unknown")
        route_l.addWidget(self.route_text)
        lay.addWidget(self.route_card)

        self.interfaces = QListWidget()
        lay.addWidget(self.interfaces)
        self.reload()

    def reload(self):
        data = self.service.status()
        self.route_text.setText(str(data.get("default_route", "unavailable")))
        self.interfaces.clear()
        for iface in data.get("interfaces", []):
            name = iface.get("name", "?")
            addrs = iface.get("addresses") or []
            self.interfaces.addItem(f"{name}: {', '.join(addrs[:3]) or 'no addresses'}")
