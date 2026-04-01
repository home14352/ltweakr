from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict

from neonctl.backend.commands import CommandRunner
from neonctl.backend.privileges import PrivilegeManager


class TweakRecord(TypedDict):
    id: str
    title: str
    description: str
    category: str
    command: list[str]


@dataclass(frozen=True)
class Tweak:
    id: str
    title: str
    description: str
    category: str
    command: tuple[str, ...]

    def as_record(self) -> TweakRecord:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "command": list(self.command),
        }


class TweaksService:
    def __init__(self) -> None:
        self.runner = CommandRunner()
        self.priv = PrivilegeManager()
        self._catalog = [tweak.as_record() for tweak in _build_tweak_catalog()]

    def status(self) -> dict:
        return {
            "supported": True,
            "count": len(self.available_tweaks()),
            "requires_root_for_apply": True,
        }

    def available_tweaks(self) -> list[dict[str, str | list[str]]]:
        return [dict(tweak) for tweak in self._catalog]

    def find_tweak(self, tweak_id: str):
        for t in self.available_tweaks():
            if t["id"] == tweak_id:
                return t
        return None

    def apply_tweak(self, tweak_id: str):
        tweak = self.find_tweak(tweak_id)
        if tweak is None:
            return None
        cmd = self.priv.wrap(list(tweak["command"]))
        return self.runner.run(cmd, timeout=180)


def _build_tweak_catalog() -> list[Tweak]:
    return [
        Tweak(
            id="lru_gen_ttl_200",
            title="Tune LRU_GEN min_ttl_ms to 200",
            description=(
                "Improves out-of-RAM behavior by asking the kernel to prefer keeping "
                "recently used pages for at least 200 ms."
            ),
            category="Memory",
            command=("python3", "-c", "open('/sys/kernel/mm/lru_gen/min_ttl_ms','w').write('200\\n')"),
        ),
        Tweak(
            id="swappiness_10",
            title="Set swappiness to 10",
            description="Reduces swap tendency on desktop systems with enough RAM.",
            category="Memory",
            command=("sysctl", "-w", "vm.swappiness=10"),
        ),
        Tweak(
            id="swappiness_20",
            title="Set swappiness to 20",
            description="Balanced swap preference for mixed desktop workloads.",
            category="Memory",
            command=("sysctl", "-w", "vm.swappiness=20"),
        ),
        Tweak(
            id="swappiness_60",
            title="Set swappiness to 60 (kernel default)",
            description="Restores a default-style swap behavior.",
            category="Memory",
            command=("sysctl", "-w", "vm.swappiness=60"),
        ),
        Tweak(
            id="vfs_cache_pressure_50",
            title="Set vfs_cache_pressure to 50",
            description="Keeps inode and dentry caches longer to reduce metadata IO.",
            category="Memory",
            command=("sysctl", "-w", "vm.vfs_cache_pressure=50"),
        ),
        Tweak(
            id="vfs_cache_pressure_100",
            title="Set vfs_cache_pressure to 100 (kernel default)",
            description="Restores default cache reclaim pressure.",
            category="Memory",
            command=("sysctl", "-w", "vm.vfs_cache_pressure=100"),
        ),
        Tweak(
            id="dirty_ratio_10",
            title="Set dirty_ratio to 10",
            description="Lowers max dirty pages to reduce long flush stalls.",
            category="Memory",
            command=("sysctl", "-w", "vm.dirty_ratio=10"),
        ),
        Tweak(
            id="dirty_bg_ratio_5",
            title="Set dirty_background_ratio to 5",
            description="Starts background writeback earlier.",
            category="Memory",
            command=("sysctl", "-w", "vm.dirty_background_ratio=5"),
        ),
        Tweak(
            id="zswap_enable",
            title="Enable zswap",
            description="Enables compressed in-RAM swap cache to reduce disk swap IO.",
            category="Memory",
            command=("sysctl", "-w", "vm.zswap.enabled=1"),
        ),
        Tweak(
            id="zswap_disable",
            title="Disable zswap",
            description="Disables compressed swap cache.",
            category="Memory",
            command=("sysctl", "-w", "vm.zswap.enabled=0"),
        ),
        Tweak(
            id="tcp_bbr",
            title="Enable TCP BBR congestion control",
            description="Uses BBR to improve throughput and latency on many links.",
            category="Network",
            command=("sysctl", "-w", "net.ipv4.tcp_congestion_control=bbr"),
        ),
        Tweak(
            id="enable_ipv6",
            title="Enable IPv6",
            description="Enables the IPv6 stack globally.",
            category="Network",
            command=("sysctl", "-w", "net.ipv6.conf.all.disable_ipv6=0"),
        ),
        Tweak(
            id="disable_ipv6",
            title="Disable IPv6",
            description="Disables the IPv6 stack globally.",
            category="Network",
            command=("sysctl", "-w", "net.ipv6.conf.all.disable_ipv6=1"),
        ),
        Tweak(
            id="restart_nm",
            title="Restart NetworkManager",
            description="Restarts NetworkManager service.",
            category="Network",
            command=("systemctl", "restart", "NetworkManager.service"),
        ),
        Tweak(
            id="trim_now",
            title="Run TRIM now",
            description="Runs fstrim on mounted filesystems.",
            category="Storage",
            command=("fstrim", "-av"),
        ),
        Tweak(
            id="enable_fstrim_timer",
            title="Enable fstrim.timer",
            description="Schedules periodic SSD TRIM.",
            category="Storage",
            command=("systemctl", "enable", "--now", "fstrim.timer"),
        ),
        Tweak(
            id="disable_fstrim_timer",
            title="Disable fstrim.timer",
            description="Stops periodic SSD TRIM scheduling.",
            category="Storage",
            command=("systemctl", "disable", "--now", "fstrim.timer"),
        ),
        Tweak(
            id="journal_vacuum_200m",
            title="Vacuum journal to 200M",
            description="Shrinks journal logs to 200 MB.",
            category="Storage",
            command=("journalctl", "--vacuum-size=200M"),
        ),
        Tweak(
            id="drop_caches",
            title="Drop filesystem caches",
            description="Runs sync and requests page cache/inode/dentry reclaim.",
            category="Storage",
            command=(
                "python3",
                "-c",
                "import os; os.sync(); open('/proc/sys/vm/drop_caches','w').write('3\\n')",
            ),
        ),
        Tweak(
            id="cpu_performance",
            title="CPU governor: performance",
            description="Switches cpufreq governor to performance.",
            category="CPU",
            command=("cpupower", "frequency-set", "-g", "performance"),
        ),
        Tweak(
            id="cpu_powersave",
            title="CPU governor: powersave",
            description="Switches cpufreq governor to powersave.",
            category="CPU",
            command=("cpupower", "frequency-set", "-g", "powersave"),
        ),
        Tweak(
            id="enable_firewalld",
            title="Enable firewalld",
            description="Enables and starts firewalld.",
            category="Services",
            command=("systemctl", "enable", "--now", "firewalld.service"),
        ),
        Tweak(
            id="disable_firewalld",
            title="Disable firewalld",
            description="Disables and stops firewalld.",
            category="Services",
            command=("systemctl", "disable", "--now", "firewalld.service"),
        ),
        Tweak(
            id="enable_bluetooth",
            title="Enable Bluetooth service",
            description="Enables and starts bluetooth.service.",
            category="Services",
            command=("systemctl", "enable", "--now", "bluetooth.service"),
        ),
        Tweak(
            id="disable_bluetooth",
            title="Disable Bluetooth service",
            description="Disables and stops bluetooth.service.",
            category="Services",
            command=("systemctl", "disable", "--now", "bluetooth.service"),
        ),
        Tweak(
            id="disable_coredumps",
            title="Disable coredumps",
            description="Disables persistent coredump storage to save disk space.",
            category="Services",
            command=("sysctl", "-w", "kernel.core_pattern=|/bin/false"),
        ),
    ]
