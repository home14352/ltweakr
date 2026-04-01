import subprocess
import time

from neonctl.backend.models import CommandResult


class CommandRunner:
    def run(self, cmd: list[str], timeout: int = 60) -> CommandResult:
        start = time.perf_counter()
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return CommandResult(
            command=cmd,
            returncode=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
            duration_s=time.perf_counter() - start,
        )
