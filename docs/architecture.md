# Architecture

This repository contains the orchestration service.

Layers:
- `api/`: request/response models and HTTP routes
- `domain/`: orchestration models and policy helpers
- `services/`: change analysis, selection, planning, execution coordination, aggregation
- `execution/`: concrete executors and command builders
- `repositories/`: config access and MongoDB persistence
- `db/`: Mongo connection and collection constants
- `integrations/`: git/event helpers and notifications

Runtime flow:
1. `/plan` or `/execute` receives a multi-repo changeset.
2. `ChangeAnalyzer` determines impacted domains.
3. `TestSelector` maps impacted domains to external test repositories.
4. `ExecutionPlanner` enriches targets with mode/profile data.
5. `ExecutionService` routes each target to a suitable executor.
6. `ResultAggregator` builds a unified summary.
7. Execution documents are stored in MongoDB.
