from orchestrator.db.collections import RUN_HISTORY_COLLECTION
from orchestrator.db.mongo import MongoConnection


class MongoRunHistoryRepository:
    def __init__(self, connection: MongoConnection | None = None) -> None:
        self.db = (connection or MongoConnection()).get_db()

    def append(self, document: dict) -> str:
        result = self.db[RUN_HISTORY_COLLECTION].insert_one(document)
        return str(result.inserted_id)

    def list_recent(self, limit: int = 50) -> list[dict]:
        cursor = self.db[RUN_HISTORY_COLLECTION].find({}, {"_id": 0}).sort("created_at", -1).limit(limit)
        return list(cursor)
