from neonctl.backend.disks import DiskService


def test_disk_status():
    assert isinstance(DiskService().status(), dict)
