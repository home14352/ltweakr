from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from neonctl.backend.tweaks import TweaksService


class TweaksPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = TweaksService()
        self.tweaks = self.service.available_tweaks()

        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("<h2>System Tweaks</h2>"))

        search_row = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search tweaks...")
        self.search.textChanged.connect(self.render_list)
        self.apply_btn = QPushButton("Apply Selected Tweak")
        self.apply_btn.clicked.connect(self.apply_selected)
        search_row.addWidget(self.search)
        search_row.addWidget(self.apply_btn)
        lay.addLayout(search_row)

        self.listing = QListWidget()
        self.listing.currentRowChanged.connect(self.show_details)
        lay.addWidget(self.listing)

        self.details = QTextEdit()
        self.details.setReadOnly(True)
        lay.addWidget(self.details)

        self.render_list()

    def filtered(self):
        q = self.search.text().lower().strip()
        if not q:
            return self.tweaks
        return [
            t
            for t in self.tweaks
            if q in str(t["title"]).lower()
            or q in str(t["id"]).lower()
            or q in str(t.get("category", "")).lower()
            or q in str(t["description"]).lower()
        ]

    def render_list(self):
        self.current = self.filtered()
        self.listing.clear()
        for tweak in self.current:
            category = tweak.get("category", "General")
            self.listing.addItem(f"[{category}] {tweak['title']}  ({tweak['id']})")
        if self.current:
            self.listing.setCurrentRow(0)
        else:
            self.details.setPlainText("No tweak matches your filter.")

    def show_details(self):
        row = self.listing.currentRow()
        if row < 0 or row >= len(self.current):
            return
        tweak = self.current[row]
        cmd = " ".join(tweak["command"])
        self.details.setPlainText(
            f"ID: {tweak['id']}\n"
            f"Title: {tweak['title']}\n\n"
            f"Category: {tweak.get('category', 'General')}\n\n"
            f"Description:\n{tweak['description']}\n\n"
            f"Command Preview:\n{cmd}\n"
        )

    def apply_selected(self):
        row = self.listing.currentRow()
        if row < 0 or row >= len(self.current):
            return
        tweak = self.current[row]
        cmd = " ".join(tweak["command"])
        if (
            QMessageBox.question(
                self,
                "Confirm tweak",
                f"Apply tweak '{tweak['title']}'?\n\n{cmd}",
            )
            != QMessageBox.StandardButton.Yes
        ):
            return

        result = self.service.apply_tweak(str(tweak["id"]))
        if result is None:
            QMessageBox.warning(self, "Tweak", "Unknown tweak selected.")
            return
        msg = f"Exit code: {result.returncode}\n\n{result.stdout or result.stderr}"
        QMessageBox.information(self, "Tweak result", msg)
