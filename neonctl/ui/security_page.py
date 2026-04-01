from neonctl.backend.security import SecurityService
from neonctl.ui.status_page import StatusPage


class SecurityPage(StatusPage):
    def __init__(self):
        super().__init__("Security", SecurityService())
