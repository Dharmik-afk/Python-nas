#!/bin/bash

# run.sh - Robust launcher for the Python File Server

# Navigate to the project root directory
cd "$(dirname "$0")/.." || exit
ROOT_DIR="$PWD"

# Determine which virtual environment to use
if [ "$USE_PYPY" = "true" ]; then
    VENV=".venv-pypy"
    INTERPRETER="PyPy 3"
else
    VENV=".venv"
    INTERPRETER="CPython 3"
fi

# Pre-flight checks
if [ ! -d "$VENV" ]; then
    echo "Error: Virtual environment '$VENV' not found. Please ensure it is set up."
    exit 1
fi

export VIRTUAL_ENV="$ROOT_DIR/$VENV"
export PATH="$VIRTUAL_ENV/bin:$PATH"

# Ensure storage directories exist
mkdir -p storage/files storage/db storage/cache logs copyparty

echo "Interpreter: $INTERPRETER"
echo "Syncing configuration..."
python3 -m app.core.user_sync

echo "Starting Supervisor..."

python3 -m supervisor.supervisor
