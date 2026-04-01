from pathlib import Path

from neonctl.backend.inventory import InventoryService
from neonctl.backend.models import PackageRecord


def test_inventory_export(tmp_path: Path):
    svc = InventoryService()
    p = tmp_path / "out.csv"
    svc.export_csv([PackageRecord(name="a", version="1")], p)
    assert p.exists()
