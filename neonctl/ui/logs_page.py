from neonctl.backend.logs import LogsService
from neonctl.ui.status_page import StatusPage


class LogsPage(StatusPage):
    def __init__(self):
        super().__init__("Logs", LogsService())
