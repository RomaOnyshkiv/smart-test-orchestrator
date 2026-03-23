from orchestrator.repositories.mongo_run_history_repository import MongoRunHistoryRepository

repo = MongoRunHistoryRepository()
repo.append(
    {
        "created_at": "2026-03-21T00:00:00Z",
        "environment": "stage",
        "results": [],
        "aggregated_summary": {"overall_status": "passed"},
    }
)
print("Seed document inserted")
