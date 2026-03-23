from orchestrator.execution.base_executor import BaseExecutor
from orchestrator.execution.executor_router import ExecutorRouter


class FakeExecutor(BaseExecutor):
    def execute(self, target):
        return {
            "execution_id": f"{target.test_repo}-{target.suite}",
            "target": target.to_dict(),
            "return_code": 0,
            "stdout": "executed",
            "stderr": "",
            "report_format": target.report_format,
        }


def test_multi_repo_execute_flow(client, monkeypatch, mongo_connection) -> None:
    monkeypatch.setattr(ExecutorRouter, "get_executor", lambda self, technology, execution_mode: FakeExecutor())

    response = client.post(
        "/execute",
        json={
            "environment": "stage",
            "changes": [
                {
                    "repo_name": "payments-service",
                    "branch": "feature/demo",
                    "changed_files": ["src/payments/checkout_service.py"],
                },
                {
                    "repo_name": "frontend-app",
                    "branch": "feature/demo",
                    "changed_files": ["src/checkout/button.tsx"],
                },
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["aggregated_summary"]["total_targets"] >= 2
    assert payload["aggregated_summary"]["overall_status"] == "passed"
