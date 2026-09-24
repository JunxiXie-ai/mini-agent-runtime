from mini_agent.tools.base import Tool


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
    with open(path, "r", encoding="utf-8") as file:
        return file.read()