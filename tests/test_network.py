from neonctl.backend.network import NetworkService


def test_network_status():
    assert isinstance(NetworkService().status(), dict)
