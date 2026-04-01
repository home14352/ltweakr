from __future__ import annotations

import shutil
from dataclasses import dataclass


@dataclass
class ManagerDef:
    name: str
    detect_bins: list[str]
    list_installed: list[str]
    search: list[str]
    install: list[str]
    remove: list[str]
    updates: list[str]


MANAGERS: dict[str, ManagerDef] = {
    "apt": ManagerDef(
        "apt",
        ["apt", "apt-get"],
        ["dpkg-query", "-W", "-f=${Package}	${Version}\n"],
        ["apt", "search"],
        ["apt", "install", "-y"],
        ["apt", "remove", "-y"],
        ["apt", "list", "--upgradable"],
    ),
    "dnf": ManagerDef(
        "dnf",
        ["dnf"],
        ["rpm", "-qa", "--qf", "%{NAME}\t%{VERSION}-%{RELEASE}.%{ARCH}\n"],
        ["dnf", "search"],
        ["dnf", "install", "-y"],
        ["dnf", "remove", "-y"],
        ["dnf", "check-update"],
    ),
    "pacman": ManagerDef(
        "pacman",
        ["pacman"],
        ["pacman", "-Q"],
        ["pacman", "-Ss"],
        ["pacman", "-S", "--noconfirm"],
        ["pacman", "-R", "--noconfirm"],
        ["pacman", "-Qu"],
    ),
    "zypper": ManagerDef(
        "zypper",
        ["zypper"],
        ["rpm", "-qa", "--qf", "%{NAME}\t%{VERSION}-%{RELEASE}.%{ARCH}\n"],
        ["zypper", "search"],
        ["zypper", "install", "-y"],
        ["zypper", "remove", "-y"],
        ["zypper", "list-updates"],
    ),
    "apk": ManagerDef(
        "apk",
        ["apk"],
        ["apk", "info", "-v"],
        ["apk", "search"],
        ["apk", "add"],
        ["apk", "del"],
        ["apk", "version", "-l", "<"],
    ),
    "xbps": ManagerDef(
        "xbps",
        ["xbps-query"],
        ["xbps-query", "-l"],
        ["xbps-query", "-Rs"],
        ["xbps-install", "-y"],
        ["xbps-remove", "-y"],
        ["xbps-install", "-Sun"],
    ),
}


def detect_native_manager() -> str | None:
    for name, mgr in MANAGERS.items():
        if all(shutil.which(b) for b in mgr.detect_bins[:1]):
            return name
    return None
