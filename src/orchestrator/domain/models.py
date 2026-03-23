from dataclasses import asdict, dataclass, field


@dataclass(slots=True)
class RepoChange:
    repo_name: str
    branch: str
    changed_files: list[str]
    commit_sha: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class MultiRepoChangeSet:
    changes: list[RepoChange]


@dataclass(slots=True)
class ExecutionTarget:
    test_repo: str
    technology: str
    suite: str
    environment: str
    execution_mode: str = "local"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class PlannedExecutionTarget(ExecutionTarget):
    timeout_seconds: int = 0
    report_format: str = "json"
    command_preview: str | None = None


@dataclass(slots=True)
class SelectionResult:
    targets: list[ExecutionTarget]
    reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class FlakyStats:
    test_name: str
    total_runs: int
    failed_runs: int
    failure_rate: float
    is_flaky: bool

    def to_dict(self) -> dict:
        return asdict(self)
