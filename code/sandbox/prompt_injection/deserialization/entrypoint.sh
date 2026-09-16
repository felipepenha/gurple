#!/bin/bash
set -e

if [ $# -gt 0 ]; then
    exec "$@"
fi

exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
