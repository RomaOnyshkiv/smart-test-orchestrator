import os
import subprocess
import uuid

from orchestrator.domain.models import PlannedExecutionTarget
from orchestrator.execution.base_executor import BaseExecutor
from orchestrator.execution.command_builders.ts_command_builder import TsCommandBuilder
from orchestrator.repositories.config_repository import ConfigRepository


class LocalTsExecutor(BaseExecutor):
    def __init__(self) -> None:
        self.config_repository = ConfigRepository()
        self.command_builder = TsCommandBuilder()

    def execute(self, target: PlannedExecutionTarget) -> dict:
        repos = self.config_repository.load_repositories()["repositories"]
        repo_config = repos[target.test_repo]
        repo_path = repo_config["path"]
        env_file = repo_config["env_files"][target.environment]
        command = self.command_builder.build(target.suite, target.environment, env_file)
        env = os.environ.copy()
        env["TARGET_ENV"] = target.environment
        env["ENV_FILE"] = env_file

        completed = subprocess.run(
            command,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False,
            env=env,
            timeout=target.timeout_seconds,
        )

        return {
            "execution_id": str(uuid.uuid4()),
            "target": target.to_dict(),
            "return_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "report_format": target.report_format,
        }
