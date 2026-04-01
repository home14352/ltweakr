from neonctl.backend.validators import valid_hostname, valid_package_name, valid_swappiness


def test_validators():
    assert valid_hostname("host-1")
    assert valid_swappiness(10)
    assert valid_package_name("python3-pip")
