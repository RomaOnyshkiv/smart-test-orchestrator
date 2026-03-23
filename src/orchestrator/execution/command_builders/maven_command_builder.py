class MavenCommandBuilder:
    def build(self, suite: str, environment: str, env_file: str) -> list[str]:
        return [
            "mvn",
            "test",
            f"-Dsuite={suite}",
            f"-Denv={environment}",
            f"-DenvFile={env_file}",
        ]
