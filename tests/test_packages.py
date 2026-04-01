from neonctl.backend.packages import PackageService


def test_package_service_instantiates():
    svc = PackageService()
    assert svc is not None
