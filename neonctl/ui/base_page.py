from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SimplePage(QWidget):
    def __init__(self, title: str, detail: str = ""):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel(f"<h2>{title}</h2>"))
        lay.addWidget(
            QLabel(
                detail or "Feature set available in backend and evolving per distro capabilities."
            )
        )
        lay.addStretch()
