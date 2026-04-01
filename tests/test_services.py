from neonctl.backend.services import ServicesService


def test_services_status():
    assert "supported" in ServicesService().status()
