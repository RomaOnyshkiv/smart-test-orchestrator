def test_plan_endpoint_returns_targets(client) -> None:
    response = client.post(
        "/plan",
        json={
            "environment": "stage",
            "changes": [
                {
                    "repo_name": "payments-service",
                    "branch": "feature/demo",
                    "changed_files": ["src/payments/checkout_service.py"],
                    "commit_sha": "abc123",
                }
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["targets"]
    assert payload["targets"][0]["test_repo"] == "payments-tests"
