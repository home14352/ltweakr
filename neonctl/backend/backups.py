from datetime import datetime
from pathlib import Path
import shutil

from neonctl.backend.paths import config_path
from neonctl.backend.paths import user_state_dir


class BackupsService:
    def status(self) -> dict:
        backup_dir = user_state_dir() / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        files = sorted(backup_dir.glob("*.bak"))
        return {
            "supported": True,
            "backup_dir": str(backup_dir),
            "backup_count": len(files),
            "backups": [f.name for f in files[-50:]],
        }

    def create_backup(self) -> Path:
        backup_dir = user_state_dir() / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        src = config_path()
        if not src.exists():
            src.write_text("")
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst = backup_dir / f"config_{stamp}.bak"
        shutil.copy2(src, dst)
        return dst
