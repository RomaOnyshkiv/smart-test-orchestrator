#!/usr/bin/env bash
set -euo pipefail

curl -X POST http://127.0.0.1:8000/execute \
  -H "Content-Type: application/json" \
  -d @examples/sample_multi_repo_request.json
