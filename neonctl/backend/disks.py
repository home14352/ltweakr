import importlib

_psutil_spec = importlib.util.find_spec("psutil")
psutil = importlib.import_module("psutil") if _psutil_spec else None


class DiskService:
    def status(self) -> dict:
        if psutil is None:
            return {"supported": False, "message": "psutil not available"}

        mounts = []
        for part in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(part.mountpoint)
                mounts.append(
                    {
                        "device": part.device,
                        "mountpoint": part.mountpoint,
                        "fstype": part.fstype,
                        "used_percent": usage.percent,
                    }
                )
            except PermissionError:
                continue

        return {"supported": True, "mounts": mounts}
