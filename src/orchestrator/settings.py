from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Smart Test Orchestrator"
    log_level: str = "INFO"

    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "smart_test_orchestrator"

    mapping_file: str = "configs/mapping.yaml"
    repositories_file: str = "configs/repositories.yaml"
    environments_file: str = "configs/environments.yaml"
    execution_profiles_file: str = "configs/execution_profiles.yaml"
    orchestrator_config_file: str = "configs/orchestrator.yaml"
    schedule_filename: str = "schedule.yaml"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
