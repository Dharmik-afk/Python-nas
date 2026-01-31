#!/bin/bash

# run.sh - Robust launcher for the Python File Server

# Navigate to the project root directory
cd "$(dirname "$0")/.." || exit
ROOT_DIR="$PWD"

# Pre-flight checks
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment '.venv' not found. Please run 'make setup' first."
    exit 1
fi

# Ensure storage directories exist
mkdir -p storage/files storage/db storage/cache logs copyparty

echo "Syncing configuration..."
uv run --no-sync python3 -m app.core.user_sync

echo "Starting Supervisor..."
uv run --no-sync python3 supervisor/supervisor.py