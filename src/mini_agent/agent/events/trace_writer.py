import json
from datetime import datetime, timezone
from pathlib import Path

from mini_agent.agent.events.types import Event


class TraceWriter:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, event: Event) -> None:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "run_id": event.run_id,
            "type": event.type,
            "data": event.data,
        }

        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")