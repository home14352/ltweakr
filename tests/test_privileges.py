from neonctl.backend.privileges import PrivilegeManager


def test_priv_methods_list():
    assert isinstance(PrivilegeManager().available_methods(), list)
