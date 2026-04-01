from neonctl.backend.capabilities import detect_capabilities


def test_capability_shape():
    c = detect_capabilities()
    assert "search" in c.package_actions
