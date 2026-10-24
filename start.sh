#!/bin/bash
cd "$(dirname "$0")"

export PLAYWRIGHT_BROWSERS_PATH="$(dirname "$0")/.ms-playwright"

source venv/bin/activate

echo "=== Starting MCP Server ==="

python main.py
