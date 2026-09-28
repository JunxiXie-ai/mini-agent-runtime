from mini_agent.tools.base import Tool
from mini_agent.tools.workspace import resolve_workspace_path


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


def list_dir(path: str) -> str:
    target = resolve_workspace_path(path)

    if not target.exists():
        return f"Directory not found: {path}"

    if not target.is_dir():
        return f"Not a directory: {path}"

    entries = sorted(target.iterdir())

    if not entries:
        return "Directory is empty."

    return "\n".join(
        f"{entry.name}/" if entry.is_dir() else entry.name
        for entry in entries
    )