from orchestrator.domain.models import ExecutionTarget, PlannedExecutionTarget
from orchestrator.repositories.config_repository import ConfigRepository


class ExecutionPlanner:
    def __init__(self, config_repository: ConfigRepository | None = None) -> None:
        self.config_repository = config_repository or ConfigRepository()

    def plan(self, targets: list[ExecutionTarget]) -> list[PlannedExecutionTarget]:
        profiles = self.config_repository.load_execution_profiles().get("profiles", {})
        planned: list[PlannedExecutionTarget] = []

        for target in targets:
            profile = profiles.get(target.technology, {})
            report_format = profile.get("report_format", "json")
            timeout_seconds = int(profile.get("timeout_seconds", 900))
            command = str(profile.get("default_command", "run-tests"))

            planned.append(
                PlannedExecutionTarget(
                    test_repo=target.test_repo,
                    technology=target.technology,
                    suite=target.suite,
                    environment=target.environment,
                    execution_mode=target.execution_mode,
                    timeout_seconds=timeout_seconds,
                    report_format=report_format,
                    command_preview=f"{command} [{target.suite}]",
                )
            )

        return planned
