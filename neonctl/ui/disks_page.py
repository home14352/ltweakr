from neonctl.backend.disks import DiskService
from neonctl.ui.status_page import StatusPage


class DisksPage(StatusPage):
    def __init__(self):
        super().__init__("Disks", DiskService())
