from dataclasses import asdict, dataclass


@dataclass(slots=True)
class ScheduleJob:

    id: str
    cron: str
    suite: str = "default"
    environment: str = "stage"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class ScheduleFile:

    repo_name: str
    repo_path: str
    jobs: list[ScheduleJob]

    def to_dict(self) -> dict:
        return {
            "repo_name": self.repo_name,
            "repo_path": self.repo_path,
            "jobs": [j.to_dict() for j in self.jobs],
        }
