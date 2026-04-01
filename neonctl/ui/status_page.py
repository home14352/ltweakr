from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)


class StatusPage(QWidget):
    def __init__(self, title: str, provider):
        super().__init__()
        self.title = title
        self.provider = provider

        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        top.addWidget(QLabel(f"<h2>{title}</h2>"))
        top.addStretch()
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        top.addWidget(self.refresh_btn)
        lay.addLayout(top)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Field", "Value"])
        self.tree.setRootIsDecorated(True)
        self.tree.setAlternatingRowColors(True)
        lay.addWidget(self.tree)

        self.refresh()

    def _append(self, parent: QTreeWidgetItem, key: str, value):
        node = QTreeWidgetItem([str(key), "" if isinstance(value, (dict, list)) else str(value)])
        parent.addChild(node)
        if isinstance(value, dict):
            for k, v in value.items():
                self._append(node, str(k), v)
        elif isinstance(value, list):
            for idx, item in enumerate(value):
                self._append(node, f"[{idx}]", item)

    def refresh(self):
        self.tree.clear()
        try:
            data = self.provider.status()
            root = QTreeWidgetItem([self.title, ""])
            self.tree.addTopLevelItem(root)
            if isinstance(data, dict):
                for k, v in data.items():
                    self._append(root, str(k), v)
            else:
                self._append(root, "value", data)
            self.tree.expandToDepth(1)
        except Exception as exc:  # noqa: BLE001
            err = QTreeWidgetItem(["error", str(exc)])
            self.tree.addTopLevelItem(err)
