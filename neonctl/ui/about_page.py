import platform

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from neonctl.backend.distro import detect_distro
from neonctl.version import VERSION


class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        d = detect_distro()
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("<h2>About NeonCtl</h2>"))
        lay.addWidget(QLabel(f"Version: {VERSION}"))
        lay.addWidget(QLabel(f"Python: {platform.python_version()}"))
        lay.addWidget(QLabel(f"Distro: {d.name}"))
        lay.addWidget(QLabel("License: MIT (project scaffold)"))
        lay.addStretch()
