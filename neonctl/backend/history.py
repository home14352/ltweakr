from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime

from neonctl.backend.models import HistoryEntry
from neonctl.backend.paths import history_path


def append_history(command: str, success: bool, summary: str) -> None:
    entry = HistoryEntry(
        when=datetime.now(UTC),
        command=command,
        success=success,
        summary=summary,
    )
    when_s = entry.when.isoformat().replace("+00:00", "Z")
    record = {
        **asdict(entry),
        "when": when_s,
    }
    with history_path().open("a") as fp:
        fp.write(json.dumps(record) + "\n")


def read_history(limit: int = 200) -> list[HistoryEntry]:
    path = history_path()
    if not path.exists():
        return []
    lines = path.read_text().splitlines()[-limit:]
    out: list[HistoryEntry] = []
    for line in lines:
        if not line.strip():
            continue
        item = json.loads(line)
        raw_when = item.get("when", "")
        parsed_when = datetime.fromisoformat(raw_when.replace("Z", "+00:00"))
        out.append(
            HistoryEntry(
                when=parsed_when,
                command=item.get("command", ""),
                success=bool(item.get("success", False)),
                summary=item.get("summary", ""),
                extra=item.get("extra", {}),
            )
        )
    out.reverse()
    return out
