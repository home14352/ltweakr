from neonctl.backend.tweaks import TweaksService
from neonctl.ui.status_page import StatusPage


class TweaksPage(StatusPage):
    def __init__(self):
        super().__init__("Tweaks", TweaksService())
