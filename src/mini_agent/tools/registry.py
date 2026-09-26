from collections.abc import Callable
from typing import Any

from mini_agent.tools.base import Tool
from mini_agent.tools.read_file import READ_FILE_TOOL, read_file
from mini_agent.tools.write_file import WRITE_FILE_TOOL, write_file


ToolFunction = Callable[..., str]


class ToolRegistry:
    def __init__(self) -> None:
        self.tools: dict[str, ToolFunction] = {}
        self.schemas: dict[str, Tool] = {}

    def register(
        self,
        schema: Tool,
        tool: ToolFunction,
    ) -> None:
        self.tools[schema.name] = tool
        self.schemas[schema.name] = schema

    def execute(self, name: str, arguments: dict[str, Any]) -> str:
        if name not in self.tools:
            return f"Unknown tool: {name}"

        tool = self.tools[name]

        return tool(**arguments)

    def get_schemas(self) -> list[Tool]:
        return list(self.schemas.values())

    def get_openai_schemas(self) -> list[dict[str, Any]]:
        return [schema.to_openai_schema() for schema in self.schemas.values()]


def create_default_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(WRITE_FILE_TOOL, write_file)
    registry.register(READ_FILE_TOOL, read_file)

    return registry