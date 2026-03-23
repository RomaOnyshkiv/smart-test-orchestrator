#!/usr/bin/env bash
set -euo pipefail

cp -n .env.example .env || true
uvicorn orchestrator.main:app --reload --app-dir src
