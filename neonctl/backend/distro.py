from pathlib import Path

from neonctl.backend.models import DistroInfo

FAMILY_MAP = {
    "fedora": "rhel",
    "rhel": "rhel",
    "centos": "rhel",
    "rocky": "rhel",
    "almalinux": "rhel",
    "ol": "rhel",
    "debian": "debian",
    "ubuntu": "debian",
    "linuxmint": "debian",
    "pop": "debian",
    "arch": "arch",
    "manjaro": "arch",
    "endeavouros": "arch",
    "opensuse-tumbleweed": "suse",
    "opensuse-leap": "suse",
    "alpine": "alpine",
    "void": "void",
    "gentoo": "gentoo",
    "nixos": "nix",
    "solus": "solus",
}


def parse_os_release(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        if "=" not in line or line.startswith("#"):
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"')
    return out


def detect_distro(path: Path = Path("/etc/os-release")) -> DistroInfo:
    if not path.exists():
        return DistroInfo()
    data = parse_os_release(path.read_text())
    distro_id = data.get("ID", "unknown")
    name = data.get("PRETTY_NAME", distro_id)
    version = data.get("VERSION_ID", "unknown")
    family = FAMILY_MAP.get(distro_id, distro_id)
    return DistroInfo(distro_id=distro_id, name=name, version=version, family=family)
