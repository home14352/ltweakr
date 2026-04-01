from neonctl.backend.desktop_integration import integration_status


def test_integration_status_keys():
    s = integration_status()
    assert "desktop" in s and "icon" in s
