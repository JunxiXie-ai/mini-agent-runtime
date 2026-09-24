from mini_agent.tools.base import Tool


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
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

    return f"File written successfully: {path}"