import pytest

from orchestrator.domain.schedule_models import ScheduleJob
from orchestrator.services.schedule_parser import parse_schedule_yaml


def test_parse_schedule_yaml_ok() -> None:
    data = {
        "schedules": [
            {"id": "nightly-smoke", "cron": "0 2 * * *", "suite": "smoke", "environment": "stage"},
            {"id": "weekly-regression", "cron": "0 4 * * 0", "suite": "full"},
        ],
    }
    out = parse_schedule_yaml(repo_name="api-tests", repo_path="/tmp/api-tests", data=data)
    assert out.repo_name == "api-tests"
    assert len(out.jobs) == 2
    assert out.jobs[0] == ScheduleJob(
        id="nightly-smoke",
        cron="0 2 * * *",
        suite="smoke",
        environment="stage",
    )
    assert out.jobs[1].environment == "stage"


def test_parse_rejects_bad_cron() -> None:
    data = {"schedules": [{"id": "bad", "cron": "0 99 99 99 99"}]}
    with pytest.raises(ValueError, match="Invalid cron"):
        parse_schedule_yaml(repo_name="x", repo_path="/x", data=data)


def test_parse_rejects_duplicate_id() -> None:
    data = {
        "schedules": [
            {"id": "same", "cron": "0 1 * * *"},
            {"id": "same", "cron": "0 2 * * *"},
        ],
    }
    with pytest.raises(ValueError, match="Duplicate"):
        parse_schedule_yaml(repo_name="x", repo_path="/x", data=data)
