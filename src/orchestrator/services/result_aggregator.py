class ResultAggregator:
    def aggregate(self, raw_results: list[dict]) -> dict:
        total_targets = len(raw_results)
        failed_targets = sum(1 for item in raw_results if item.get("return_code", 1) != 0)
        passed_targets = total_targets - failed_targets

        return {
            "total_targets": total_targets,
            "passed_targets": passed_targets,
            "failed_targets": failed_targets,
            "overall_status": "failed" if failed_targets else "passed",
        }
