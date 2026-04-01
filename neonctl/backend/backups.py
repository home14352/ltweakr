from neonctl.backend.paths import user_state_dir


class BackupsService:
    def status(self) -> dict:
        backup_dir = user_state_dir() / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        files = sorted(backup_dir.glob("*.bak"))
        return {"supported": True, "backup_dir": str(backup_dir), "backup_count": len(files)}
