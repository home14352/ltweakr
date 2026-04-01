import importlib
import time

_psutil_spec = importlib.util.find_spec("psutil")
psutil = importlib.import_module("psutil") if _psutil_spec else None


def collect_stats() -> dict:
    if psutil is None:
        return {
            "cpu_percent": 0.0,
            "ram_percent": 0.0,
            "ram_used_gb": 0.0,
            "ram_total_gb": 0.0,
            "disk_root_percent": 0.0,
            "uptime_s": 0,
        }

    vm = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    boot = psutil.boot_time()
    uptime = int(time.time() - boot)
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.0),
        "ram_percent": vm.percent,
        "ram_used_gb": round(vm.used / (1024**3), 2),
        "ram_total_gb": round(vm.total / (1024**3), 2),
        "disk_root_percent": disk.percent,
        "uptime_s": uptime,
    }
