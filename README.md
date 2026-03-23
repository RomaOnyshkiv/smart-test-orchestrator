# !!! It's just a concept, not a working product!!!
# Smart Test Orchestrator

A multi-repository test orchestration skeleton for QA/Platform engineering.

This project acts as a central control plane that:
- analyzes changes across source repositories
- selects test targets from external test repositories
- supports Python, Java/Maven, and TypeScript test execution
- runs against environment-specific configs and env files
- stores execution history and reports in MongoDB

## Architecture at a glance

```text
Client/Webhook -> ChangeAnalyzer -> TestSelector -> ExecutionPlanner -> ExecutionService
                                                            |-> Python executor
                                                            |-> Maven executor
                                                            |-> TypeScript executor
                                                            |-> GitHub Actions executor (stub)
                                                     -> ResultAggregator -> MongoDB
```

## What lives in this repository

This repository contains the orchestrator service itself and tests for the orchestrator.
It does **not** contain the external AUT test suites. Those are modeled through config files in `configs/`.

## Supported concepts

- multi-repo changesets
- environment-aware selection (`stage`, `prodlike`, `dev`)
- technology-aware execution (`python`, `java`, `typescript`)
- local execution and remote workflow dispatch abstraction
- MongoDB persistence for executions, reports, run history, and flaky stats

## Quick start

### 1. Prepare environment

```bash
cp .env.example .env
```

### 2. Start services

```bash
docker compose up -d --build
```

### 3. Run API locally without Docker

```bash
make install
make run
```

### 4. Health check

```bash
curl http://127.0.0.1:8000/health
```

### 5. Planning example

```bash
make demo-plan
```

### 6. Execution example

```bash
make demo-execute
```

## Example request body

See `examples/sample_multi_repo_request.json`.

## Notes

- Local executors assume external test repositories are already available on disk at paths configured in `configs/repositories.yaml`.
- For a real implementation, replace env files with a secrets manager or CI secret store.
- Remote execution is intentionally modeled behind an abstraction and the GitHub Actions executor is a stub.

## Why this project matters

This is not just a test framework.

It demonstrates a shift from:
- “run all tests everywhere”

to:
- “analyze change impact and run the right tests in the right repository and environment.”
