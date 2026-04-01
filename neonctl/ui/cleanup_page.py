from neonctl.backend.cleanup import CleanupService
from neonctl.ui.status_page import StatusPage


class CleanupPage(StatusPage):
    def __init__(self):
        super().__init__("Cleanup", CleanupService())
