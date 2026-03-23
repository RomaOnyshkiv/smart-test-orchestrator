from orchestrator.execution.github_actions_executor import GitHubActionsExecutor
from orchestrator.execution.local_maven_executor import LocalMavenExecutor
from orchestrator.execution.local_python_executor import LocalPythonExecutor
from orchestrator.execution.local_ts_executor import LocalTsExecutor


class ExecutorRouter:
    def __init__(self) -> None:
        self.python_executor = LocalPythonExecutor()
        self.maven_executor = LocalMavenExecutor()
        self.ts_executor = LocalTsExecutor()
        self.github_executor = GitHubActionsExecutor()

    def get_executor(self, technology: str, execution_mode: str):
        if execution_mode == "github_actions":
            return self.github_executor
        if technology == "python":
            return self.python_executor
        if technology == "java":
            return self.maven_executor
        if technology == "typescript":
            return self.ts_executor
        raise ValueError(f"Unsupported technology: {technology}")
