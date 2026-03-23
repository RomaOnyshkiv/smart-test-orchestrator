from orchestrator.db.collections import FLAKY_STATS_COLLECTION
from orchestrator.db.mongo import MongoConnection


class MongoFlakyRepository:
    def __init__(self, connection: MongoConnection | None = None) -> None:
        self.db = (connection or MongoConnection()).get_db()

    def save_many(self, documents: list[dict]) -> int:
        if not documents:
            return 0
        result = self.db[FLAKY_STATS_COLLECTION].insert_many(documents)
        return len(result.inserted_ids)
