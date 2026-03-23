from orchestrator.services.result_aggregator import ResultAggregator


def test_result_aggregator_counts_results() -> None:
    aggregator = ResultAggregator()
    result = aggregator.aggregate(
        [
            {"return_code": 0},
            {"return_code": 1},
        ]
    )

    assert result["total_targets"] == 2
    assert result["failed_targets"] == 1
    assert result["overall_status"] == "failed"
