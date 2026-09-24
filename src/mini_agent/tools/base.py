from dataclasses import dataclass
from typing import Any

@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]