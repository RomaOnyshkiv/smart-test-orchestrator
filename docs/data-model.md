# Data Model

MongoDB collections:
- `executions`: execution documents for full runs
- `run_history`: append-only history of run events
- `reports`: generated reports
- `flaky_stats`: derived flaky metrics

Execution document example:
- created_at
- environment
- changes
- selected_targets
- planned_targets
- results
- aggregated_summary
