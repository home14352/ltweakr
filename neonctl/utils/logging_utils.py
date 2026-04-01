import logging
from pathlib import Path

from neonctl.backend.paths import user_state_dir


def setup_logging() -> None:
    log_dir = user_state_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    logfile = Path(log_dir) / "neonctl.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.FileHandler(logfile), logging.StreamHandler()],
    )
