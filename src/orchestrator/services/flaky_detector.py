from orchestrator.domain.models import FlakyStats


class FlakyDetector:
    def analyze(self, history: list[dict], min_runs: int = 3, threshold: float = 0.2) -> list[FlakyStats]:
        aggregated: dict[str, dict[str, int]] = {}

        for run in history:
            for result in run.get("results", []):
                target = result.get("target", {})
                test_name = f"{target.get('test_repo', 'unknown')}::{target.get('suite', 'unknown')}"
                aggregated.setdefault(test_name, {"total": 0, "failed": 0})
                aggregated[test_name]["total"] += 1
                if result.get("return_code", 1) != 0:
                    aggregated[test_name]["failed"] += 1

        stats: list[FlakyStats] = []
        for test_name, values in aggregated.items():
            total = values["total"]
            failed = values["failed"]
            failure_rate = failed / total if total else 0.0
            stats.append(
                FlakyStats(
                    test_name=test_name,
                    total_runs=total,
                    failed_runs=failed,
                    failure_rate=failure_rate,
                    is_flaky=total >= min_runs and 0 < failure_rate < 1 and failure_rate >= threshold,
                )
            )

        return sorted(stats, key=lambda item: item.failure_rate, reverse=True)
