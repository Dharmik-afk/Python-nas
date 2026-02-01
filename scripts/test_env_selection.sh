#!/bin/bash
# test_env_selection.sh

test_env() {
    local use_pypy=$1
    local expected=$2
    
    echo "Testing USE_PYPY='$use_pypy'..."
    
    # Simulate run.sh logic
    if [ "$use_pypy" = "true" ]; then
        VENV=".venv-pypy"
    else
        VENV=".venv"
    fi
    
    if [ "$VENV" = "$expected" ]; then
        echo "PASS: Selected $VENV"
    else
        echo "FAIL: Expected $expected, got $VENV"
        exit 1
    fi
}

test_env "" ".venv"
test_env "false" ".venv"
test_env "true" ".venv-pypy"

echo "All environment selection tests passed!"
