from pathlib import Path

from orchestrator.repositories.config_repository import ConfigRepository
from orchestrator.services.schedule_repo_scanner import ScheduleRepoScanner


def test_scan_all_loads_schedule_yaml(tmp_path: Path, monkeypatch) -> None:
    test_repo = tmp_path / "fake-tests"
    test_repo.mkdir()
    (test_repo / "schedule.yaml").write_text(
        """
schedules:
  - id: nightly
    cron: "0 3 * * *"
    suite: smoke
    environment: stage
""",
        encoding="utf-8",
    )

    repos_yaml = tmp_path / "repositories.yaml"
    repos_yaml.write_text(
        f"""
repositories:
  fake-tests:
    type: test-repo
    technology: python
    execution_mode: local
    path: {test_repo}
    default_branch: main
""",
        encoding="utf-8",
    )

    class _Cfg(ConfigRepository):
        def __init__(self) -> None:
            self.repositories_file = str(repos_yaml)

    scanner = ScheduleRepoScanner(config=_Cfg())
    found = scanner.scan_all()
    assert len(found) == 1
    assert found[0].repo_name == "fake-tests"
    assert found[0].jobs[0].id == "nightly"
