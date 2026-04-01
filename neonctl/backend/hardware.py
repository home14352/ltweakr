import platform


class HardwareService:
    def status(self) -> dict:
        return {
            "supported": True,
            "machine": platform.machine(),
            "processor": platform.processor() or "unknown",
            "platform": platform.platform(),
        }
