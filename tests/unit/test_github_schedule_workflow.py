from orchestrator.domain.schedule_models import ScheduleFile, ScheduleJob
from orchestrator.services.github_schedule_workflow import render_schedule_workflow


def test_render_schedule_workflow_one_job_per_entry() -> None:
    schedule = ScheduleFile(
        repo_name="api-tests",
        repo_path="/x",
        jobs=[
            ScheduleJob(id="a", cron="0 2 * * *", suite="smoke", environment="stage"),
            ScheduleJob(id="b", cron="0 4 * * 0", suite="full", environment="prodlike"),
        ],
    )
    yaml_text = render_schedule_workflow(schedule)
    assert "on:" in yaml_text
    assert "schedule:" in yaml_text
    assert "workflow_dispatch:" in yaml_text
    assert "a:" in yaml_text
    assert "b:" in yaml_text
    assert "github.event.schedule == '0 2 * * *'" in yaml_text
    assert "runs-on: ubuntu-latest" in yaml_text
    assert '"smoke"' in yaml_text or "smoke" in yaml_text
