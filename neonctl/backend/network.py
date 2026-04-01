import importlib
import shutil

from neonctl.backend.commands import CommandRunner

_psutil_spec = importlib.util.find_spec("psutil")
psutil = importlib.import_module("psutil") if _psutil_spec else None


class NetworkService:
    def __init__(self) -> None:
        self.runner = CommandRunner()

    def status(self) -> dict:
        interfaces = []
        if psutil is not None:
            for iface, addrs in psutil.net_if_addrs().items():
                ips = [a.address for a in addrs if getattr(a, "family", None) is not None]
                interfaces.append({"name": iface, "addresses": ips[:3]})

        default_route = "unavailable"
        if shutil.which("ip"):
            res = self.runner.run(["ip", "route", "show", "default"], timeout=10)
            if res.returncode == 0 and res.stdout.strip():
                default_route = res.stdout.splitlines()[0].strip()

        return {
            "supported": True,
            "interfaces": interfaces,
            "default_route": default_route,
        }
