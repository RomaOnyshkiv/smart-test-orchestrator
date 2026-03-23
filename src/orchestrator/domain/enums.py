from enum import StrEnum


class Technology(StrEnum):
    PYTHON = "python"
    JAVA = "java"
    TYPESCRIPT = "typescript"


class ExecutionMode(StrEnum):
    LOCAL = "local"
    GITHUB_ACTIONS = "github_actions"
