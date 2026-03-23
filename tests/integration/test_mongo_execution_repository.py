def test_mongo_execution_repository_saves_document(execution_repo) -> None:
    inserted_id = execution_repo.save({"execution_id": "abc", "results": []})
    assert inserted_id
