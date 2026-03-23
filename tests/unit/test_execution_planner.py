from orchestrator.domain.models import ExecutionTarget
from orchestrator.services.execution_planner import ExecutionPlanner


def test_execution_planner_enriches_targets() -> None:
    planner = ExecutionPlanner()
    planned = planner.plan(
        [
            ExecutionTarget(
                test_repo="api-tests",
                technology="python",
                suite="smoke",
                environment="stage",
            )
        ]
    )

    assert planned[0].timeout_seconds > 0
    assert planned[0].report_format == "json"
