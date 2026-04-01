import importlib

_psutil_spec = importlib.util.find_spec("psutil")
psutil = importlib.import_module("psutil") if _psutil_spec else None


class ProcessesService:
    def status(self) -> dict:
        if psutil is None:
            return {"supported": False, "message": "psutil unavailable"}
        top = []
        for proc in psutil.process_iter(["pid", "name", "username"]):
            info = proc.info
            top.append({
                "pid": str(info.get("pid")),
                "name": info.get("name") or "?",
                "user": info.get("username") or "?",
            })
            if len(top) >= 20:
                break
        return {"supported": True, "process_count": len(psutil.pids()), "sample": top}
