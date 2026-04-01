import importlib

from neonctl.backend.commands import CommandRunner
from neonctl.backend.privileges import PrivilegeManager

_psutil_spec = importlib.util.find_spec("psutil")
psutil = importlib.import_module("psutil") if _psutil_spec else None


class ProcessesService:
    def __init__(self) -> None:
        self.runner = CommandRunner()
        self.priv = PrivilegeManager()

    def status(self) -> dict:
        if psutil is None:
            return {"supported": False, "message": "psutil unavailable"}
        return {
            "supported": True,
            "process_count": len(psutil.pids()),
            "cpu_percent": psutil.cpu_percent(interval=0.0),
            "ram_percent": psutil.virtual_memory().percent,
        }

    def list_processes(self, limit: int = 300) -> list[dict[str, str]]:
        if psutil is None:
            return []
        rows = []
        for proc in psutil.process_iter(
            ["pid", "name", "username", "memory_percent", "cpu_percent"]
        ):
            info = proc.info
            rows.append(
                {
                    "pid": str(info.get("pid", "")),
                    "name": str(info.get("name") or "?"),
                    "user": str(info.get("username") or "?"),
                    "cpu": f"{float(info.get('cpu_percent') or 0.0):.1f}",
                    "mem": f"{float(info.get('memory_percent') or 0.0):.1f}",
                }
            )
            if len(rows) >= limit:
                break
        return rows

    def terminate(self, pid: int) -> bool:
        if psutil is None:
            return False
        try:
            p = psutil.Process(pid)
            p.terminate()
            p.wait(timeout=3)
            return True
        except Exception:  # noqa: BLE001
            return False

    def clean_ram(self) -> bool:
        cmd = [
            "python3",
            "-c",
            "import os; os.sync(); open('/proc/sys/vm/drop_caches','w').write('3\\n')",
        ]
        wrapped = self.priv.wrap(cmd)
        res = self.runner.run(wrapped, timeout=120)
        return res.returncode == 0
