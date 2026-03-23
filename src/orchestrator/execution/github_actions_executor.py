import uuid

from orchestrator.domain.models import PlannedExecutionTarget
from orchestrator.execution.base_executor import BaseExecutor


class GitHubActionsExecutor(BaseExecutor):
    def execute(self, target: PlannedExecutionTarget) -> dict:
        return {
            "execution_id": str(uuid.uuid4()),
            "target": target.to_dict(),
            "return_code": 0,
            "stdout": f"Triggered remote workflow for {target.test_repo}:{target.suite}",
            "stderr": "",
            "report_format": target.report_format,
            "status": "triggered",
        }
