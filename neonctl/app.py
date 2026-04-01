import sys

from PySide6.QtWidgets import QApplication

from neonctl.ui.main_window import MainWindow


def run() -> int:
    app = QApplication(sys.argv)
    w = MainWindow()
    if not w.settings.start_minimized_to_tray:
        w.show()
    return app.exec()
