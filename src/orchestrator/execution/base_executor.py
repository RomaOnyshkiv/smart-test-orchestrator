from abc import ABC, abstractmethod

from orchestrator.domain.models import PlannedExecutionTarget


class BaseExecutor(ABC):
    @abstractmethod
    def execute(self, target: PlannedExecutionTarget) -> dict:
        raise NotImplementedError
