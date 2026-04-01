import re
from pathlib import Path


def valid_hostname(value: str) -> bool:
    return bool(re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9-]{0,62}", value))


def valid_swappiness(value: int) -> bool:
    return 0 <= value <= 100


def valid_repo_url(url: str) -> bool:
    return url.startswith(("http://", "https://", "file://"))


def valid_package_name(name: str) -> bool:
    return bool(re.fullmatch(r"[a-zA-Z0-9.+_-]+", name))


def valid_path(path: str) -> bool:
    return Path(path).expanduser().exists()
