from pydantic import BaseModel, Field


class RepoChangeRequest(BaseModel):
    repo_name: str
    branch: str
    changed_files: list[str] = Field(default_factory=list)
    commit_sha: str | None = None


class PlanRequest(BaseModel):
    environment: str = "stage"
    changes: list[RepoChangeRequest]


class PlanResponse(BaseModel):
    impacted_domains: list[dict]
    targets: list[dict]
    reasons: list[str]


class ExecuteResponse(BaseModel):
    execution_results: list[dict]
    aggregated_summary: dict
    report_id: str | None = None
    flaky_candidates: list[dict] = Field(default_factory=list)


class ScheduleScanResponse(BaseModel):
    repositories: list[dict]


class ScheduleWorkflowPreviewResponse(BaseModel):
    repo_name: str
    workflow_yaml: str
