from neonctl.backend.updates import UpdateService


def test_updates_instantiates():
    assert isinstance(UpdateService().list_updates(), list)
