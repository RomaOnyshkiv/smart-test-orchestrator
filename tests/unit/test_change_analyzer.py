from orchestrator.domain.models import MultiRepoChangeSet, RepoChange
from orchestrator.services.change_analyzer import ChangeAnalyzer


def test_change_analyzer_finds_impacted_domains() -> None:
    analyzer = ChangeAnalyzer()
    changeset = MultiRepoChangeSet(
        changes=[
            RepoChange(
                repo_name="payments-service",
                branch="feature/demo",
                changed_files=["src/payments/checkout_service.py"],
            )
        ]
    )

    result = analyzer.analyze(changeset)

    assert result["impacted_domains"]
    assert result["impacted_domains"][0]["domain"] == "payments-service"
