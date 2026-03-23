from orchestrator.domain.models import MultiRepoChangeSet
from orchestrator.repositories.config_repository import ConfigRepository


class ChangeAnalyzer:
    def __init__(self, config_repository: ConfigRepository | None = None) -> None:
        self.config_repository = config_repository or ConfigRepository()

    def analyze(self, changeset: MultiRepoChangeSet) -> dict:
        mapping = self.config_repository.load_mapping()
        impacted_domains: list[dict] = []
        seen: set[tuple[str, str]] = set()

        for domain_name, domain_config in mapping.get("mappings", {}).items():
            affected_by = domain_config.get("affected_by", [])

            for repo_change in changeset.changes:
                for rule in affected_by:
                    if rule.get("repo") != repo_change.repo_name:
                        continue

                    configured_paths = rule.get("paths", [])
                    matched = any(
                        changed_file.startswith(path_prefix)
                        for changed_file in repo_change.changed_files
                        for path_prefix in configured_paths
                    )
                    if not matched:
                        continue

                    key = (domain_name, repo_change.repo_name)
                    if key in seen:
                        continue
                    seen.add(key)

                    impacted_domains.append(
                        {
                            "domain": domain_name,
                            "source_repo": repo_change.repo_name,
                            "branch": repo_change.branch,
                            "commit_sha": repo_change.commit_sha,
                        }
                    )
                    break

        return {"impacted_domains": impacted_domains}
