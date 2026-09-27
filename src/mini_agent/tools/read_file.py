from mini_agent.tools.base import Tool
from mini_agent.tools.workspace import resolve_workspace_path


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


def read_file(path: str) -> str:
    target = resolve_workspace_path(path)

    if not target.exists():
        return f"File not found: {path}"

    if not target.is_file():
        return f"Not a file: {path}"

    return target.read_text(encoding="utf-8")