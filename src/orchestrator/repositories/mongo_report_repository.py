from orchestrator.db.collections import REPORTS_COLLECTION
from orchestrator.db.mongo import MongoConnection


class MongoReportRepository:
    def __init__(self, connection: MongoConnection | None = None) -> None:
        self.db = (connection or MongoConnection()).get_db()

    def save(self, document: dict) -> str:
        result = self.db[REPORTS_COLLECTION].insert_one(document)
        return str(result.inserted_id)
