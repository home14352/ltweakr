from __future__ import annotations

from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from neonctl.backend.flatpak import FlatpakService


class FlatpakPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = FlatpakService()

        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        self.query = QLineEdit()
        self.query.setPlaceholderText("Flatpak app id or search term")
        self.search_btn = QPushButton("Search")
        self.install_btn = QPushButton("Install")
        self.remove_btn = QPushButton("Remove")
        self.list_btn = QPushButton("List Installed")
        self.search_btn.clicked.connect(self.search)
        self.install_btn.clicked.connect(self.install)
        self.remove_btn.clicked.connect(self.remove)
        self.list_btn.clicked.connect(self.reload_installed)
        top.addWidget(self.query)
        for b in [self.search_btn, self.install_btn, self.remove_btn, self.list_btn]:
            top.addWidget(b)
        lay.addLayout(top)

        lists = QHBoxLayout()
        installed_box = QGroupBox("Installed")
        installed_l = QVBoxLayout(installed_box)
        self.installed = QListWidget()
        self.installed.itemClicked.connect(lambda item: self.query.setText(item.text()))
        installed_l.addWidget(self.installed)
        lists.addWidget(installed_box)

        search_box = QGroupBox("Search results")
        search_l = QVBoxLayout(search_box)
        self.search_results = QListWidget()
        self.search_results.itemClicked.connect(self._pick_search_result)
        search_l.addWidget(self.search_results)
        lists.addWidget(search_box)
        lay.addLayout(lists)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        lay.addWidget(self.output)
        self.reload_installed()

    def _append_result(self, title: str, res):
        self.output.append(f"\n=== {title} ===")
        self.output.append(f"rc={res.returncode}")
        if res.stdout.strip():
            self.output.append(res.stdout.strip())
        if res.stderr.strip():
            self.output.append(res.stderr.strip())

    def search(self):
        q = self.query.text().strip()
        if not q:
            return
        res = self.service.search(q)
        self._append_result("Flatpak search", res)
        self.search_results.clear()
        if res.returncode == 0:
            for line in res.stdout.splitlines()[1:]:
                if line.strip():
                    self.search_results.addItem(line.strip())

    def install(self):
        q = self.query.text().strip()
        if not q:
            return
        if QMessageBox.question(self, "Install", f"Install {q}?") != QMessageBox.StandardButton.Yes:
            return
        self._append_result("Flatpak install", self.service.install(q))

    def remove(self):
        q = self.query.text().strip()
        if not q:
            return
        if QMessageBox.question(self, "Remove", f"Remove {q}?") != QMessageBox.StandardButton.Yes:
            return
        self._append_result("Flatpak remove", self.service.remove(q))

    def reload_installed(self):
        rows = self.service.list_installed()
        self.installed.clear()
        self.installed.addItems(rows)
        self.output.setPlainText("Installed Flatpak apps:\n" + "\n".join(rows))

    def _pick_search_result(self, item):
        token = item.text().split()[-1]
        self.query.setText(token)
