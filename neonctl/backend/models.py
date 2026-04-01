from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str
    duration_s: float


@dataclass(slots=True)
class DistroInfo:
    distro_id: str = "unknown"
    name: str = "Unknown"
    version: str = "unknown"
    family: str = "unknown"


@dataclass(slots=True)
class PackageRecord:
    name: str
    version: str = "unknown"
    arch: str = "unknown"
    source: str = "unknown"
    size: str = "unknown"
    reason: str = "unknown"


@dataclass(slots=True)
class CapabilityMatrix:
    native_manager: str
    package_actions: dict[str, bool]
    service_actions: dict[str, bool]
    privilege_methods: list[str]
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class HistoryEntry:
    when: datetime
    command: str
    success: bool
    summary: str
    extra: dict[str, Any] = field(default_factory=dict)
