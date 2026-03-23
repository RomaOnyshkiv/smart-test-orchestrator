class GitHubEventParser:
    def parse(self, payload: dict) -> dict:
        return {
            "repo_name": payload.get("repository"),
            "branch": payload.get("branch"),
            "changed_files": payload.get("changed_files", []),
            "commit_sha": payload.get("commit_sha"),
        }
