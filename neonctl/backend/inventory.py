import csv
from pathlib import Path

from neonctl.backend.models import PackageRecord
from neonctl.backend.packages import PackageService


class InventoryService:
    def __init__(self) -> None:
        self.pkg = PackageService()

    def all_installed(self) -> list[PackageRecord]:
        return self.pkg.list_installed()

    def export_csv(self, records: list[PackageRecord], path: Path) -> None:
        with path.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["name", "version", "arch", "source", "size", "reason"])
            for r in records:
                w.writerow([r.name, r.version, r.arch, r.source, r.size, r.reason])
