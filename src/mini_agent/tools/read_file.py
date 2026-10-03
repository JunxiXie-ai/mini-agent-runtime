from mini_agent.tools.base import Tool
from mini_agent.tools.workspace import resolve_workspace_path
from mini_agent.tools.result import ToolResult


READ_FILE_TOOL = Tool(
    name="read_file",
    description="Read text content from a file.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path of the file to read.",
            }
        },
        "required": ["path"],
    },
)


def read_file(path: str) -> ToolResult:
    target = resolve_workspace_path(path)

    if not target.exists():
        return ToolResult(success=False, output=f"File not found: {path}")

    if not target.is_file():
        return ToolResult(success=False, output=f"Not a file: {path}")

    return ToolResult(success=True, output=target.read_text(encoding="utf-8"))