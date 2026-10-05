from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class Session:
    id: str = field(default_factory=lambda: uuid4().hex)
    messages: list[dict[str, Any]] = field(default_factory=list)