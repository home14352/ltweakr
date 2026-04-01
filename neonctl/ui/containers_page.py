from neonctl.backend.containers import ContainersService
from neonctl.ui.status_page import StatusPage


class ContainersPage(StatusPage):
    def __init__(self):
        super().__init__("Containers", ContainersService())
