from PySide6.QtWidgets import QGridLayout, QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from neonctl.backend.desktop import detect_desktop_environment, session_type
from neonctl.backend.distro import detect_distro
from neonctl.backend.monitoring import collect_stats
from neonctl.utils.formatters import human_duration


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        top = QHBoxLayout()
        top.addWidget(QLabel("<h2>Dashboard</h2>"))
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        top.addWidget(self.refresh_btn)
        top.addStretch()
        self.layout.addLayout(top)
        grid = QGridLayout()
        self.distro_lbl = QLabel()
        self.desktop_lbl = QLabel()
        self.cpu_lbl = QLabel()
        self.ram_lbl = QLabel()
        self.disk_lbl = QLabel()
        self.uptime_lbl = QLabel()
        cards = [
            ("Distro", self.distro_lbl),
            ("Desktop session", self.desktop_lbl),
            ("CPU", self.cpu_lbl),
            ("RAM", self.ram_lbl),
            ("Disk /", self.disk_lbl),
            ("Uptime", self.uptime_lbl),
        ]
        for idx, (title, value_lbl) in enumerate(cards):
            box = QGroupBox(title)
            b = QVBoxLayout(box)
            b.addWidget(value_lbl)
            grid.addWidget(box, idx // 2, idx % 2)
        self.layout.addLayout(grid)
        self.layout.addStretch()
        self.refresh()

    def refresh(self):
        d = detect_distro()
        s = collect_stats()
        self.distro_lbl.setText(f"{d.name} ({d.family})")
        self.desktop_lbl.setText(f"{detect_desktop_environment()} ({session_type()})")
        self.cpu_lbl.setText(f"{s['cpu_percent']}%")
        self.ram_lbl.setText(f"{s['ram_percent']}% ({s['ram_used_gb']}/{s['ram_total_gb']} GB)")
        self.disk_lbl.setText(f"{s['disk_root_percent']}%")
        self.uptime_lbl.setText(human_duration(s["uptime_s"]))
