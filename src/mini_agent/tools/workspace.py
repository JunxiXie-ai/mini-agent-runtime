from pathlib import Path


WORKSPACE_ROOT = Path("workspace").resolve()


def resolve_workspace_path(path: str) -> Path:
    WORKSPACE_ROOT.mkdir(exist_ok=True)

    target = (WORKSPACE_ROOT / path).resolve()

    if target != WORKSPACE_ROOT and WORKSPACE_ROOT not in target.parents:
        raise ValueError("Path escapes workspace")

    return target