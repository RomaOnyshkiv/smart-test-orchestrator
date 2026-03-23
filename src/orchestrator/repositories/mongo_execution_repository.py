from orchestrator.db.collections import EXECUTIONS_COLLECTION
from orchestrator.db.mongo import MongoConnection


class MongoExecutionRepository:
    def __init__(self, connection: MongoConnection | None = None) -> None:
        self.db = (connection or MongoConnection()).get_db()

    def save(self, document: dict) -> str:
        result = self.db[EXECUTIONS_COLLECTION].insert_one(document)
        return str(result.inserted_id)

    def find_by_execution_id(self, execution_id: str) -> dict | None:
        return self.db[EXECUTIONS_COLLECTION].find_one({"execution_id": execution_id}, {"_id": 0})
