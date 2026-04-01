from neonctl.backend.backups import BackupsService
from neonctl.ui.status_page import StatusPage


class BackupsPage(StatusPage):
    def __init__(self):
        super().__init__("Backups", BackupsService())
