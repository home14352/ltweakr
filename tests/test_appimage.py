from neonctl.backend.appimage import AppImageService


def test_appimage_status():
    assert isinstance(AppImageService().status(), dict)
