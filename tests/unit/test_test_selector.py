from orchestrator.services.test_selector import TestSelector


def test_selector_returns_targets_for_stage() -> None:
    selector = TestSelector()

    selection = selector.select(
        impacted_domains=[{"domain": "user-api", "source_repo": "user-api", "branch": "feature/demo"}],
        requested_environment="stage",
    )

    assert selection.targets
    assert selection.targets[0].test_repo == "api-tests"
    assert selection.targets[0].environment == "stage"
