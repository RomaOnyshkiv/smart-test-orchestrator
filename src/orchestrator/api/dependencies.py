from orchestrator.services.change_analyzer import ChangeAnalyzer
from orchestrator.services.execution_planner import ExecutionPlanner
from orchestrator.services.execution_service import ExecutionService
from orchestrator.services.flaky_detector import FlakyDetector
from orchestrator.services.report_service import ReportService
from orchestrator.services.result_aggregator import ResultAggregator
from orchestrator.services.test_selector import TestSelector


def get_change_analyzer() -> ChangeAnalyzer:
    return ChangeAnalyzer()


def get_test_selector() -> TestSelector:
    return TestSelector()


def get_execution_planner() -> ExecutionPlanner:
    return ExecutionPlanner()


def get_execution_service() -> ExecutionService:
    return ExecutionService()


def get_result_aggregator() -> ResultAggregator:
    return ResultAggregator()


def get_flaky_detector() -> FlakyDetector:
    return FlakyDetector()


def get_report_service() -> ReportService:
    return ReportService()
