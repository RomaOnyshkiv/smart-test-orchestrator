class OrchestratorError(Exception):
    """Base orchestrator exception."""


class ConfigError(OrchestratorError):
    """Raised when config is invalid or missing."""


class ExecutionError(OrchestratorError):
    """Raised when execution fails unexpectedly."""
