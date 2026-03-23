from pathlib import Path

from orchestrator.settings import get_settings


class RepoScanner:
    """Filesystem helpers for configured test repositories."""

    def __init__(self, schedule_filename: str | None = None) -> None:
        self._schedule_filename = schedule_filename or get_settings().schedule_filename

    def exists(self, path: str) -> bool:
        return Path(path).exists()

    def schedule_file_path(self, repo_path: str) -> Path:
        return Path(repo_path) / self._schedule_filename

    def has_schedule_file(self, repo_path: str) -> bool:
        return self.schedule_file_path(repo_path).is_file()
