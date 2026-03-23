# Execution Flow

`/execute` creates a `MultiRepoChangeSet`, analyzes impact, selects targets, enriches them into planned targets, executes them, aggregates results, stores them in Mongo, and returns a concise summary.
