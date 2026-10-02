from mini_agent.tools.base import Tool
from mini_agent.tools.workspace import resolve_workspace_path
from mini_agent.tools.result import ToolResult

LIST_DIR_TOOL = Tool(
    name="list_dir",
    description="List files and directories inside a workspace directory.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Directory path relative to the workspace.",
            }
        },
        "required": ["path"],
    },
)


def list_dir(path: str) -> ToolResult:
    target = resolve_workspace_path(path)

    if not target.exists():
        return ToolResult(success=False, output=f"Directory not found: {path}")

    if not target.is_dir():
        return ToolResult(success=False, output=f"Not a directory: {path}")

    entries = sorted(target.iterdir())

    if not entries:
        return ToolResult(success=True, output="Directory is empty.")

    return ToolResult(success=True, output="\n".join(
        f"{entry.name}/" if entry.is_dir() else entry.name
        for entry in entries
    ))