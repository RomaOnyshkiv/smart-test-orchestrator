from pymongo import MongoClient

from orchestrator.settings import get_settings


class MongoConnection:
    def __init__(self, client: MongoClient | None = None) -> None:
        settings = get_settings()
        self.client = client or MongoClient(settings.mongo_uri)
        self.db = self.client[settings.mongo_db_name]

    def get_db(self):
        return self.db
