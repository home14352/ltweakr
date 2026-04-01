from pathlib import Path

from neonctl.backend.commands import CommandRunner
from neonctl.backend.models import CommandResult


class AppImageService:
    def __init__(self) -> None:
        self.runner = CommandRunner()

    def scan_paths(self) -> list[Path]:
        return [Path.home() / "Applications", Path.home() / "Downloads"]

    def list_appimages(self) -> list[Path]:
        files: list[Path] = []
        for root in self.scan_paths():
            if not root.exists():
                continue
            files.extend(root.glob("*.AppImage"))
        return sorted(files)

    def status(self) -> dict:
        files = self.list_appimages()
        return {
            "supported": True,
            "count": len(files),
            "scan_paths": [str(r) for r in self.scan_paths()],
        }

    def make_executable(self, path: Path) -> bool:
        try:
            path.chmod(path.stat().st_mode | 0o111)
            return True
        except OSError:
            return False

    def launch(self, path: Path) -> CommandResult:
        return self.runner.run([str(path)], timeout=30)
