from pathlib import Path

from neonctl.backend.distro import detect_distro, parse_os_release


def test_parse_os_release():
    d = parse_os_release('ID=ubuntu\nVERSION_ID="24.04"\n')
    assert d["ID"] == "ubuntu"


def test_detect_distro(tmp_path: Path):
    p = tmp_path / "os-release"
    p.write_text('ID=arch\nPRETTY_NAME="Arch Linux"\nVERSION_ID=rolling\n')
    info = detect_distro(p)
    assert info.family == "arch"
