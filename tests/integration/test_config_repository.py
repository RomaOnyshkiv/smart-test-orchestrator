from orchestrator.repositories.config_repository import ConfigRepository


def test_config_repository_loads_mapping() -> None:
    repo = ConfigRepository()
    mapping = repo.load_mapping()
    assert "mappings" in mapping
