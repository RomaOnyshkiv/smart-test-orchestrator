from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from croniter import CroniterBadCronError, croniter

from orchestrator.domain.schedule_models import ScheduleFile, ScheduleJob
from orchestrator.utils.yaml_loader import load_yaml


def _validate_cron(expression: str) -> str:
    expr = expression.strip()
    parts = expr.split()
    if len(parts) != 5:
        msg = "GitHub Actions cron must have exactly five fields (minute hour day month weekday)"
        raise ValueError(msg)
    try:
        croniter(expr, datetime.now(UTC))
    except CroniterBadCronError as exc:
        raise ValueError(f"Invalid cron expression: {expression!r}") from exc
    return expr


def _normalize_job_id(raw: str) -> str:
    s = raw.strip().lower().replace(" ", "-")
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-_")
    if not s or not all(c in allowed for c in s):
        raise ValueError(
            f"Job id must be non-empty and only contain [a-z0-9-_], got {raw!r}",
        )
    return s


def parse_schedule_yaml(
    *,
    repo_name: str,
    repo_path: str,
    data: dict[str, Any],
) -> ScheduleFile:
    raw = data.get("schedules")
    if raw is None:
        raise ValueError("schedule.yaml must contain a top-level 'schedules' list")
    if not isinstance(raw, list):
        raise ValueError("'schedules' must be a list")
    jobs: list[ScheduleJob] = []
    seen: set[str] = set()
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("Each schedule entry must be a mapping")
        job_id = _normalize_job_id(str(item.get("id", "")))
        if job_id in seen:
            raise ValueError(f"Duplicate schedule job id: {job_id}")
        seen.add(job_id)
        cron_raw = item.get("cron")
        if not isinstance(cron_raw, str) or not cron_raw.strip():
            raise ValueError(f"Missing or invalid 'cron' for job {job_id!r}")
        cron = _validate_cron(cron_raw)
        suite = str(item.get("suite", "default"))
        environment = str(item.get("environment", "stage"))
        jobs.append(
            ScheduleJob(
                id=job_id,
                cron=cron,
                suite=suite,
                environment=environment,
            ),
        )
    return ScheduleFile(repo_name=repo_name, repo_path=repo_path, jobs=jobs)


def load_schedule_file(path: str | Path) -> dict[str, Any]:
    return load_yaml(path)


def parse_schedule_file(
    *,
    repo_name: str,
    repo_path: str,
    file_path: str | Path,
) -> ScheduleFile:
    data = load_schedule_file(file_path)
    return parse_schedule_yaml(repo_name=repo_name, repo_path=repo_path, data=data)
