"""Generate GitHub Actions workflow YAML from a parsed schedule.yaml.

Each schedule entry becomes one job. On ``workflow_dispatch``, every job runs in
parallel. On ``schedule``, only jobs whose ``cron`` matches ``github.event.schedule`` run
(``github.event.schedule`` is the cron expression that triggered the run).
"""

from __future__ import annotations

import json
import textwrap

from orchestrator.domain.schedule_models import ScheduleFile


def _yaml_scalar(value: str) -> str:
    return json.dumps(value)


def render_schedule_workflow(
    schedule: ScheduleFile,
    *,
    workflow_name: str | None = None,
) -> str:
    if not schedule.jobs:
        raise ValueError("schedule.yaml must define at least one job")

    name = workflow_name or f"Scheduled tests ({schedule.repo_name})"

    job_blocks = []
    for job in schedule.jobs:
        condition = (
            "github.event_name == 'workflow_dispatch' || "
            f"github.event.schedule == '{job.cron}'"
        )
        block = textwrap.dedent(
            f"""\
            {job.id}:
              if: {condition}
              runs-on: ubuntu-latest
              env:
                SUITE: {_yaml_scalar(job.suite)}
                ENVIRONMENT: {_yaml_scalar(job.environment)}
                TEST_REPO: {_yaml_scalar(schedule.repo_name)}
              steps:
                - name: Run scheduled suite (stub)
                  run: |
                    echo "Scheduled job {job.id} for repo $TEST_REPO"
                    echo "suite=$SUITE environment=$ENVIRONMENT"
            """,
        ).rstrip()
        job_blocks.append(block)

    jobs_yaml = "\n\n".join(job_blocks)

    schedule_lines = [f"    - cron: '{job.cron}'" for job in schedule.jobs]
    header = "\n".join(
        [
            f"name: {json.dumps(name)}",
            "",
            "on:",
            "  schedule:",
            *schedule_lines,
            "  workflow_dispatch:",
            "",
            "jobs:",
            textwrap.indent(jobs_yaml, "  "),
        ],
    )
    return header + "\n"
