from orchestrator.execution.base_executor import BaseExecutor
from orchestrator.execution.executor_router import ExecutorRouter


class FakeExecutor(BaseExecutor):
    def execute(self, target):
        return {
            "execution_id": "fake-id",
            "target": target.to_dict(),
            "return_code": 0,
            "stdout": "ok",
            "stderr": "",
            "report_format": target.report_format,
        }


def test_execute_endpoint_returns_summary(client, monkeypatch, mongo_connection) -> None:
    monkeypatch.setattr(ExecutorRouter, "get_executor", lambda self, technology, execution_mode: FakeExecutor())

    response = client.post(
        "/execute",
        json={
            "environment": "stage",
            "changes": [
                {
                    "repo_name": "user-api",
                    "branch": "feature/demo",
                    "changed_files": ["app/api/users.py"],
                }
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["aggregated_summary"]["overall_status"] == "passed"
    assert payload["execution_results"]
