import subprocess

from mini_agent.tools.base import Tool
from mini_agent.tools.workspace import WORKSPACE_ROOT, resolve_workspace_path


RUN_PYTHON_TOOL = Tool(
    name="run_python",
    description="Run a Python file inside the workspace and return its output.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Python file path relative to the workspace.",
            }
        },
        "required": ["path"],
    },
)


def run_python(path: str) -> str:
    target = resolve_workspace_path(path)

    if not target.exists():
        return f"File not found: {path}"

    if not target.is_file():
        return f"Not a file: {path}"

    if target.suffix != ".py":
        return f"Not a Python file: {path}"

    result = subprocess.run(
        ["python", str(target)],
        cwd=WORKSPACE_ROOT,
        capture_output=True,
        text=True,
        timeout=10,
    )

    output = result.stdout

    if result.stderr:
        output += result.stderr

    return output or f"Process exited with code {result.returncode}"