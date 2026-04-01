from neonctl.backend.snap import SnapService


def test_snap_status():
    assert isinstance(SnapService().status(), dict)
