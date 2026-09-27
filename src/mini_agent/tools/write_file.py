from mini_agent.tools.base import Tool
from mini_agent.tools.workspace import resolve_workspace_path


WRITE_FILE_TOOL = Tool(
    name="write_file",
    description="Write text content to a file.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path of the file to write.",
            },
            "content": {
                "type": "string",
                "description": "Text content to write into the file.",
            },
        },
        "required": ["path", "content"],
    },
)


def write_file(path: str, content: str) -> str:
    target = resolve_workspace_path(path)

    target.parent.mkdir(parents=True, exist_ok=True)

    target.write_text(
        content,
        encoding="utf-8",
    )

    return f"File written successfully: {path}"