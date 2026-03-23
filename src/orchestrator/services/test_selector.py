from orchestrator.domain.models import ExecutionTarget, SelectionResult
from orchestrator.repositories.config_repository import ConfigRepository


class TestSelector:
    def __init__(self, config_repository: ConfigRepository | None = None) -> None:
        self.config_repository = config_repository or ConfigRepository()

    def select(
        self,
        impacted_domains: list[dict],
        requested_environment: str,
    ) -> SelectionResult:
        mapping = self.config_repository.load_mapping()
        repositories = self.config_repository.load_repositories().get("repositories", {})
        targets: list[ExecutionTarget] = []
        reasons: list[str] = []

        for impacted in impacted_domains:
            domain_name = impacted["domain"]
            domain_config = mapping["mappings"].get(domain_name, {})
            domain_tests = domain_config.get("tests", [])

            for test_config in domain_tests:
                if requested_environment not in test_config.get("environments", []):
                    continue

                repo_name = test_config["test_repo"]
                repo_config = repositories.get(repo_name, {})
                execution_mode = repo_config.get("execution_mode", "local")

                for suite in test_config.get("suites", []):
                    targets.append(
                        ExecutionTarget(
                            test_repo=repo_name,
                            technology=test_config["technology"],
                            suite=suite,
                            environment=requested_environment,
                            execution_mode=execution_mode,
                        )
                    )

                reasons.append(
                    f"Domain '{domain_name}' maps to repo '{repo_name}' for environment '{requested_environment}'"
                )

        return SelectionResult(targets=self._deduplicate(targets), reasons=reasons)

    @staticmethod
    def _deduplicate(targets: list[ExecutionTarget]) -> list[ExecutionTarget]:
        seen: set[tuple[str, str, str, str, str]] = set()
        unique: list[ExecutionTarget] = []

        for target in targets:
            key = (
                target.test_repo,
                target.technology,
                target.suite,
                target.environment,
                target.execution_mode,
            )
            if key in seen:
                continue
            seen.add(key)
            unique.append(target)

        return unique
