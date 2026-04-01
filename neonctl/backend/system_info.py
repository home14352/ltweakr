import platform


class SystemInfoService:
    def status(self) -> dict:
        return {
            "supported": True,
            "system": platform.system(),
            "release": platform.release(),
            "python": platform.python_version(),
        }
