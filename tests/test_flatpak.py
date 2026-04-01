from neonctl.backend.flatpak import FlatpakService


def test_flatpak_status():
    assert isinstance(FlatpakService().status(), dict)
