from collections.abc import Callable
from typing import Any

from mini_agent.tools.read_file import read_file
from mini_agent.tools.write_file import write_file


ToolFunction = Callable[..., str]


class ToolRegistry:
    def __init__(self) -> None:
        self.tools: dict[str, ToolFunction] = {}

    def register(self, name: str, tool: ToolFunction) -> None:
        self.tools[name] = tool

    def execute(self, name: str, arguments: dict[str, Any]) -> str:
        if name not in self.tools:
            return f"Unknown tool: {name}"

        tool = self.tools[name]

        return tool(**arguments)


def create_default_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register("write_file", write_file)
    registry.register("read_file", read_file)

    return registry