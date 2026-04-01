from __future__ import annotations

from neonctl.backend.commands import CommandRunner
from neonctl.backend.privileges import PrivilegeManager


class TweaksService:
    def __init__(self) -> None:
        self.runner = CommandRunner()
        self.priv = PrivilegeManager()

    def status(self) -> dict:
        return {
            "supported": True,
            "count": len(self.available_tweaks()),
            "requires_root_for_apply": True,
        }

    def available_tweaks(self) -> list[dict[str, str | list[str]]]:
        return [
            {
                "id": "lru_gen_ttl_200",
                "title": "Set LRU_GEN min_ttl_ms = 200",
                "description": "Writes 200 to /sys/kernel/mm/lru_gen/min_ttl_ms.",
                "command": [
                    "python3",
                    "-c",
                    "open('/sys/kernel/mm/lru_gen/min_ttl_ms','w').write('200\\n')",
                ],
            },
            {
                "id": "swappiness_10",
                "title": "Set swappiness=10",
                "description": "Lower swap use.",
                "command": ["sysctl", "-w", "vm.swappiness=10"],
            },
            {
                "id": "swappiness_20",
                "title": "Set swappiness=20",
                "description": "Balanced swap setting.",
                "command": ["sysctl", "-w", "vm.swappiness=20"],
            },
            {
                "id": "swappiness_60",
                "title": "Set swappiness=60",
                "description": "Kernel default style value.",
                "command": ["sysctl", "-w", "vm.swappiness=60"],
            },
            {
                "id": "vfs_cache_pressure_50",
                "title": "Set vfs_cache_pressure=50",
                "description": "Keep inode/dentry cache longer.",
                "command": ["sysctl", "-w", "vm.vfs_cache_pressure=50"],
            },
            {
                "id": "vfs_cache_pressure_100",
                "title": "Set vfs_cache_pressure=100",
                "description": "Kernel default pressure.",
                "command": ["sysctl", "-w", "vm.vfs_cache_pressure=100"],
            },
            {
                "id": "dirty_ratio_10",
                "title": "Set dirty_ratio=10",
                "description": "Reduce max dirty pages.",
                "command": ["sysctl", "-w", "vm.dirty_ratio=10"],
            },
            {
                "id": "dirty_bg_ratio_5",
                "title": "Set dirty_background_ratio=5",
                "description": "Flush dirty pages earlier.",
                "command": ["sysctl", "-w", "vm.dirty_background_ratio=5"],
            },
            {
                "id": "tcp_bbr",
                "title": "Enable TCP BBR",
                "description": "Use BBR congestion control.",
                "command": ["sysctl", "-w", "net.ipv4.tcp_congestion_control=bbr"],
            },
            {
                "id": "enable_ipv6",
                "title": "Enable IPv6",
                "description": "Enable IPv6 stack.",
                "command": ["sysctl", "-w", "net.ipv6.conf.all.disable_ipv6=0"],
            },
            {
                "id": "disable_ipv6",
                "title": "Disable IPv6",
                "description": "Disable IPv6 stack.",
                "command": ["sysctl", "-w", "net.ipv6.conf.all.disable_ipv6=1"],
            },
            {
                "id": "trim_now",
                "title": "Run TRIM now",
                "description": "Run fstrim over mounted FS.",
                "command": ["fstrim", "-av"],
            },
            {
                "id": "restart_nm",
                "title": "Restart NetworkManager",
                "description": "Restart NM service.",
                "command": ["systemctl", "restart", "NetworkManager.service"],
            },
            {
                "id": "enable_firewalld",
                "title": "Enable firewalld",
                "description": "Enable firewalld now and at boot.",
                "command": ["systemctl", "enable", "--now", "firewalld.service"],
            },
            {
                "id": "disable_firewalld",
                "title": "Disable firewalld",
                "description": "Disable firewalld now and at boot.",
                "command": ["systemctl", "disable", "--now", "firewalld.service"],
            },
            {
                "id": "enable_bluetooth",
                "title": "Enable bluetooth",
                "description": "Enable bluetooth service.",
                "command": ["systemctl", "enable", "--now", "bluetooth.service"],
            },
            {
                "id": "disable_bluetooth",
                "title": "Disable bluetooth",
                "description": "Disable bluetooth service.",
                "command": ["systemctl", "disable", "--now", "bluetooth.service"],
            },
            {
                "id": "enable_fstrim_timer",
                "title": "Enable fstrim.timer",
                "description": "Periodic SSD trim.",
                "command": ["systemctl", "enable", "--now", "fstrim.timer"],
            },
            {
                "id": "disable_fstrim_timer",
                "title": "Disable fstrim.timer",
                "description": "Disable periodic trim.",
                "command": ["systemctl", "disable", "--now", "fstrim.timer"],
            },
            {
                "id": "journal_vacuum_200m",
                "title": "Vacuum journal to 200M",
                "description": "Reduce journal size.",
                "command": ["journalctl", "--vacuum-size=200M"],
            },
            {
                "id": "drop_caches",
                "title": "Drop page cache",
                "description": "Sync + drop filesystem caches.",
                "command": [
                    "python3",
                    "-c",
                    "import os; os.sync(); open('/proc/sys/vm/drop_caches','w').write('3\\n')",
                ],
            },
            {
                "id": "cpu_performance",
                "title": "CPU governor performance",
                "description": "Set performance governor via cpupower.",
                "command": ["cpupower", "frequency-set", "-g", "performance"],
            },
            {
                "id": "cpu_powersave",
                "title": "CPU governor powersave",
                "description": "Set powersave governor via cpupower.",
                "command": ["cpupower", "frequency-set", "-g", "powersave"],
            },
        ]

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
