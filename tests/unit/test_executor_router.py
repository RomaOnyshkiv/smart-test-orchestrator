from orchestrator.execution.executor_router import ExecutorRouter
from orchestrator.execution.local_python_executor import LocalPythonExecutor


def test_executor_router_returns_python_executor() -> None:
    router = ExecutorRouter()
    executor = router.get_executor("python", "local")
    assert isinstance(executor, LocalPythonExecutor)
