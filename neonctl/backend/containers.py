import shutil


class ContainersService:
    def status(self) -> dict:
        tools = {
            "docker": bool(shutil.which("docker")),
            "podman": bool(shutil.which("podman")),
            "distrobox": bool(shutil.which("distrobox")),
            "toolbox": bool(shutil.which("toolbox")),
        }
        return {
            "supported": True,
            "tools": tools,
            "available_count": sum(1 for v in tools.values() if v),
        }
