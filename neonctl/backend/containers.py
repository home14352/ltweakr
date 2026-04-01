import shutil

from neonctl.backend.commands import CommandRunner


class ContainersService:
    def __init__(self) -> None:
        self.runner = CommandRunner()

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

    def list_containers(self, engine: str) -> list[str]:
        if not shutil.which(engine):
            return []
        res = self.runner.run([engine, "ps", "-a", "--format", "{{.Names}}\t{{.Status}}"], timeout=30)
        if res.returncode != 0:
            return []
        return [ln for ln in res.stdout.splitlines() if ln.strip()]

    def run_action(self, engine: str, action: str, name: str):
        if not shutil.which(engine):
            return None
        if action not in {"start", "stop", "restart", "rm"}:
            return None
        return self.runner.run([engine, action, name], timeout=120)
