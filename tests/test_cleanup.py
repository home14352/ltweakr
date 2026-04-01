from neonctl.backend.cleanup import CleanupService


def test_cleanup_status():
    assert isinstance(CleanupService().status(), dict)
