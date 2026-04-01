from neonctl.backend.processes import ProcessesService
from neonctl.ui.status_page import StatusPage


class ProcessesPage(StatusPage):
    def __init__(self):
        super().__init__("Processes", ProcessesService())
