class PythonCommandBuilder:
    def build(self, suite: str, environment: str, env_file: str) -> list[str]:
        return ["pytest", "-m", suite, f"--env={environment}", f"--env-file={env_file}"]
