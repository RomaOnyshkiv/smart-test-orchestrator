from orchestrator.services.flaky_detector import FlakyDetector


def test_flaky_detector_marks_candidate() -> None:
    detector = FlakyDetector()
    history = [
        {"results": [{"target": {"test_repo": "api-tests", "suite": "smoke"}, "return_code": 0}]},
        {"results": [{"target": {"test_repo": "api-tests", "suite": "smoke"}, "return_code": 1}]},
        {"results": [{"target": {"test_repo": "api-tests", "suite": "smoke"}, "return_code": 0}]},
    ]

    result = detector.analyze(history, min_runs=3, threshold=0.2)

    assert result
    assert result[0].is_flaky is True
