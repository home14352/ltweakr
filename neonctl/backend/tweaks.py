import locale
import socket
import time


class TweaksService:
    def status(self) -> dict:
        tz = time.tzname[0] if time.tzname else "unknown"
        loc = locale.getlocale()
        return {
            "supported": True,
            "hostname": socket.gethostname(),
            "timezone": tz,
            "locale": str(loc),
        }
