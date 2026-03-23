from orchestrator.execution.executor_router import ExecutorRouter


class ExecutionService:
    def __init__(self, router: ExecutorRouter | None = None) -> None:
        self.router = router or ExecutorRouter()

    def execute_targets(self, targets: list) -> list[dict]:
        results: list[dict] = []
        for target in targets:
            executor = self.router.get_executor(target.technology, target.execution_mode)
            results.append(executor.execute(target))
        return results
