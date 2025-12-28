#!/bin/bash

# run.sh - Robust launcher for the Python File Server

# Navigate to the project root directory (one level up from scripts/)
cd "$(dirname "$0")/.." || exit
ROOT_DIR="$PWD"

# Pre-flight checks
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment 'venv' not found. Please run 'make setup' first."
    exit 1
fi

# Ensure storage directories exist
mkdir -p storage/files storage/db storage/cache logs copyparty

echo "Starting Supervisor..."
source venv/bin/activate
python3 supervisor/supervisor.py