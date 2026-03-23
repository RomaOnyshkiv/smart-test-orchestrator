from pathlib import Path

from fastapi.testclient import TestClient

from orchestrator.settings import get_settings


def test_scan_schedules_endpoint(tmp_path: Path, client: TestClient, monkeypatch) -> None:
    test_repo = tmp_path / "demo-tests"
    test_repo.mkdir()
    (test_repo / "schedule.yaml").write_text(
        """
schedules:
  - id: nightly
    cron: "0 5 * * *"
    suite: smoke
    environment: stage
""",
        encoding="utf-8",
    )

    repos_yaml = tmp_path / "repositories.yaml"
    repos_yaml.write_text(
        f"""
repositories:
  demo-tests:
    type: test-repo
    technology: python
    execution_mode: local
    path: {test_repo}
    default_branch: main
""",
        encoding="utf-8",
    )

    monkeypatch.setenv("REPOSITORIES_FILE", str(repos_yaml))
    get_settings.cache_clear()

    response = client.get("/schedules/scan")
    assert response.status_code == 200
    body = response.json()
    assert body["repositories"]
    assert body["repositories"][0]["repo_name"] == "demo-tests"
    assert body["repositories"][0]["jobs"][0]["id"] == "nightly"


def test_workflow_preview_not_found(client: TestClient) -> None:
    response = client.get("/schedules/workflow-preview", params={"repo_name": "nonexistent"})
    assert response.status_code == 404
