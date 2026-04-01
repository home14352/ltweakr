from neonctl.backend import autostart


def test_autostart_path_name():
    assert autostart.autostart_path().name == "neonctl.desktop"
