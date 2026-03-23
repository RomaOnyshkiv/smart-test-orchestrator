from orchestrator.settings import get_settings
from orchestrator.utils.yaml_loader import load_yaml


class ConfigRepository:
    def __init__(self) -> None:
        settings = get_settings()
        self.mapping_file = settings.mapping_file
        self.repositories_file = settings.repositories_file
        self.environments_file = settings.environments_file
        self.execution_profiles_file = settings.execution_profiles_file
        self.orchestrator_config_file = settings.orchestrator_config_file

    def load_mapping(self) -> dict:
        return load_yaml(self.mapping_file)

    def load_repositories(self) -> dict:
        return load_yaml(self.repositories_file)

    def load_environments(self) -> dict:
        return load_yaml(self.environments_file)

    def load_execution_profiles(self) -> dict:
        return load_yaml(self.execution_profiles_file)

    def load_orchestrator_config(self) -> dict:
        return load_yaml(self.orchestrator_config_file)
