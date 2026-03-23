from orchestrator.repositories.mongo_report_repository import MongoReportRepository
from orchestrator.utils.time_utils import utc_now_iso


class ReportService:
    def __init__(self, repository: MongoReportRepository | None = None) -> None:
        self.repository = repository or MongoReportRepository()

    def create_report(self, execution_document: dict, flaky_candidates: list[dict]) -> str:
        report = {
            "created_at": utc_now_iso(),
            "environment": execution_document.get("environment"),
            "aggregated_summary": execution_document.get("aggregated_summary", {}),
            "selected_targets": execution_document.get("selected_targets", []),
            "flaky_candidates": flaky_candidates,
        }
        return self.repository.save(report)
