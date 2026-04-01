from neonctl.backend.network import NetworkService
from neonctl.ui.status_page import StatusPage


class NetworkPage(StatusPage):
    def __init__(self):
        super().__init__("Network", NetworkService())
