from pathlib import Path

from neonctl.backend.appimage import AppImageService


def test_appimage_status():
    assert isinstance(AppImageService().status(), dict)


def test_make_executable(tmp_path: Path):
    f = tmp_path / "tool.AppImage"
    f.write_text("x")
    svc = AppImageService()
    assert svc.make_executable(f)
