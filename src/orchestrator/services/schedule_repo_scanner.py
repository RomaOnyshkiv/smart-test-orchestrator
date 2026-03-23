from pathlib import Path

from orchestrator.domain.schedule_models import ScheduleFile
from orchestrator.repositories.config_repository import ConfigRepository
from orchestrator.services.schedule_parser import parse_schedule_file
from orchestrator.settings import get_settings
from orchestrator.utils.path_utils import resolve_repo_path


class ScheduleRepoScanner:
    """Loads ``schedule.yaml`` from each configured test repository path."""

    def __init__(self, *, config: ConfigRepository | None = None) -> None:
        self._config = config or ConfigRepository()
        self._filename = get_settings().schedule_filename

    def scan_all(self) -> list[ScheduleFile]:
        repos = self._config.load_repositories().get("repositories", {})
        results: list[ScheduleFile] = []
        for repo_name, meta in repos.items():
            if not isinstance(meta, dict):
                continue
            if meta.get("type") != "test-repo":
                continue
            path = meta.get("path")
            if not isinstance(path, str) or not path.strip():
                continue
            resolved = resolve_repo_path(path)
            schedule_path = Path(resolved) / self._filename
            if not schedule_path.is_file():
                continue
            parsed = parse_schedule_file(
                repo_name=repo_name,
                repo_path=resolved,
                file_path=schedule_path,
            )
            results.append(parsed)
        return results
