#!/usr/bin/env bash
# Dev runner: starts the backend (uvicorn) and a static file server for the frontend.
# Usage: ./scripts/dev.sh
# Requires: ANTHROPIC_API_KEY set in environment.

set -e

if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$GOOGLE_API_KEY" ]; then
    echo "ERROR: Set ANTHROPIC_API_KEY or GOOGLE_API_KEY." >&2
    exit 1
fi

trap 'kill 0' EXIT

echo "Starting backend on http://localhost:8000 ..."
uv run uvicorn cv_mcp.api:app --reload --port 8000 &

echo "Starting frontend on http://localhost:5173 ..."
python3 -m http.server 5173 -d frontend &

echo ""
echo "Ready:"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo "  Health:   http://localhost:8000/health"
echo "  MCP:      http://localhost:8000/mcp"
echo ""

wait
