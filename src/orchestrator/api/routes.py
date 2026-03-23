from fastapi import APIRouter, HTTPException

from orchestrator.api.schemas import (
    ExecuteResponse,
    PlanRequest,
    PlanResponse,
    ScheduleScanResponse,
    ScheduleWorkflowPreviewResponse,
)
from orchestrator.domain.models import MultiRepoChangeSet, RepoChange
from orchestrator.repositories.mongo_execution_repository import MongoExecutionRepository
from orchestrator.repositories.mongo_run_history_repository import MongoRunHistoryRepository
from orchestrator.services.change_analyzer import ChangeAnalyzer
from orchestrator.services.execution_planner import ExecutionPlanner
from orchestrator.services.execution_service import ExecutionService
from orchestrator.services.flaky_detector import FlakyDetector
from orchestrator.services.github_schedule_workflow import render_schedule_workflow
from orchestrator.services.report_service import ReportService
from orchestrator.services.result_aggregator import ResultAggregator
from orchestrator.services.schedule_repo_scanner import ScheduleRepoScanner
from orchestrator.services.test_selector import TestSelector
from orchestrator.utils.time_utils import utc_now_iso

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/schedules/scan", response_model=ScheduleScanResponse)
def scan_schedules() -> ScheduleScanResponse:
    """Discover ``schedule.yaml`` under configured test repo paths and parse cron jobs."""
    scanner = ScheduleRepoScanner()
    found = scanner.scan_all()
    return ScheduleScanResponse(repositories=[s.to_dict() for s in found])


@router.get("/schedules/workflow-preview", response_model=ScheduleWorkflowPreviewResponse)
def schedule_workflow_preview(repo_name: str) -> ScheduleWorkflowPreviewResponse:
    """Return GitHub Actions workflow YAML: one job per schedule entry (parallel on dispatch)."""
    scanner = ScheduleRepoScanner()
    for schedule in scanner.scan_all():
        if schedule.repo_name == repo_name:
            yaml_text = render_schedule_workflow(schedule)
            return ScheduleWorkflowPreviewResponse(repo_name=repo_name, workflow_yaml=yaml_text)
    raise HTTPException(
        status_code=404,
        detail=f"No schedule.yaml found or no jobs for repository {repo_name!r}",
    )


@router.post("/plan", response_model=PlanResponse)
def plan(request: PlanRequest) -> PlanResponse:
    changeset = MultiRepoChangeSet(
        changes=[
            RepoChange(
                repo_name=item.repo_name,
                branch=item.branch,
                changed_files=item.changed_files,
                commit_sha=item.commit_sha,
            )
            for item in request.changes
        ]
    )

    analyzer = ChangeAnalyzer()
    selector = TestSelector()

    analysis = analyzer.analyze(changeset)
    selection = selector.select(
        impacted_domains=analysis["impacted_domains"],
        requested_environment=request.environment,
    )

    return PlanResponse(
        impacted_domains=analysis["impacted_domains"],
        targets=[target.to_dict() for target in selection.targets],
        reasons=selection.reasons,
    )


@router.post("/execute", response_model=ExecuteResponse)
def execute(request: PlanRequest) -> ExecuteResponse:
    changeset = MultiRepoChangeSet(
        changes=[
            RepoChange(
                repo_name=item.repo_name,
                branch=item.branch,
                changed_files=item.changed_files,
                commit_sha=item.commit_sha,
            )
            for item in request.changes
        ]
    )

    analyzer = ChangeAnalyzer()
    selector = TestSelector()
    planner = ExecutionPlanner()
    execution_service = ExecutionService()
    aggregator = ResultAggregator()
    flaky_detector = FlakyDetector()
    report_service = ReportService()

    execution_repo = MongoExecutionRepository()
    history_repo = MongoRunHistoryRepository()

    analysis = analyzer.analyze(changeset)
    selection = selector.select(
        impacted_domains=analysis["impacted_domains"],
        requested_environment=request.environment,
    )
    planned_targets = planner.plan(selection.targets)

    raw_results = execution_service.execute_targets(planned_targets)
    aggregated = aggregator.aggregate(raw_results)

    document = {
        "created_at": utc_now_iso(),
        "environment": request.environment,
        "changes": [change.to_dict() for change in changeset.changes],
        "impacted_domains": analysis["impacted_domains"],
        "selected_targets": [target.to_dict() for target in selection.targets],
        "planned_targets": [target.to_dict() for target in planned_targets],
        "results": raw_results,
        "aggregated_summary": aggregated,
    }

    execution_repo.save(document)
    history_repo.append(document)

    recent_history = history_repo.list_recent(limit=50)
    flaky_candidates = [item.to_dict() for item in flaky_detector.analyze(recent_history)]
    report_id = report_service.create_report(document, flaky_candidates)

    return ExecuteResponse(
        execution_results=raw_results,
        aggregated_summary=aggregated,
        report_id=report_id,
        flaky_candidates=flaky_candidates,
    )
