class TsCommandBuilder:
    def build(self, suite: str, environment: str, env_file: str) -> list[str]:
        return ["npm", "test", "--", f"--suite={suite}", f"--env={environment}", f"--envFile={env_file}"]
