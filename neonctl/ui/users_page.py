from neonctl.backend.users import UsersService
from neonctl.ui.status_page import StatusPage


class UsersPage(StatusPage):
    def __init__(self):
        super().__init__("Users", UsersService())
