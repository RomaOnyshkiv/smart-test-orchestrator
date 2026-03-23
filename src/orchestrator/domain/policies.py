def default_suite_priority(technology: str) -> list[str]:
    if technology == "python":
        return ["smoke", "contract", "regression"]
    if technology == "java":
        return ["smoke", "regression"]
    if technology == "typescript":
        return ["critical-path", "regression"]
    return ["smoke", "regression"]
