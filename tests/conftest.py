import mongomock
import pytest
from fastapi.testclient import TestClient

from orchestrator.db.mongo import MongoConnection
from orchestrator.main import app
from orchestrator.repositories.mongo_execution_repository import MongoExecutionRepository
from orchestrator.repositories.mongo_report_repository import MongoReportRepository
from orchestrator.repositories.mongo_run_history_repository import MongoRunHistoryRepository


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def mongo_connection(monkeypatch):
    fake_client = mongomock.MongoClient()

    def fake_init(self, client=None):
        self.client = fake_client
        self.db = fake_client["smart_test_orchestrator_test"]

    monkeypatch.setattr(MongoConnection, "__init__", fake_init)
    return MongoConnection()


@pytest.fixture
def execution_repo(mongo_connection):
    return MongoExecutionRepository(connection=mongo_connection)


@pytest.fixture
def history_repo(mongo_connection):
    return MongoRunHistoryRepository(connection=mongo_connection)


@pytest.fixture
def report_repo(mongo_connection):
    return MongoReportRepository(connection=mongo_connection)
