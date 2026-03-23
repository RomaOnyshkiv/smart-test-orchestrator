from pathlib import Path


def resolve_repo_path(path: str) -> str:
    return str(Path(path).expanduser().resolve())
