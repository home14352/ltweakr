from neonctl.backend.commands import CommandRunner
from neonctl.backend.package_managers import MANAGERS, detect_native_manager


class UpdateService:
    def __init__(self) -> None:
        self.runner = CommandRunner()
        self.manager = detect_native_manager()

    def list_updates(self) -> list[str]:
        if not self.manager:
            return []
        res = self.runner.run(MANAGERS[self.manager].updates, timeout=90)
        if res.returncode != 0:
            return []
        return [ln for ln in res.stdout.splitlines() if ln.strip()]
