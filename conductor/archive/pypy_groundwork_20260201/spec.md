# Specification: PyPy Groundwork & Runtime Logic

## Overview
Establish the foundational support for PyPy 3.12, including environment setup and dynamic interpreter switching in the build system.

## Goals
- Audit all dependencies for PyPy compatibility.
- Implement dynamic runtime switching in the `Makefile` and `scripts/run.sh`.
- Default to standard CPython.

## Functional Requirements
- **Dependency Compatibility:** Perform a compatibility audit of the current `pyproject.toml`. Identify and resolve any issues with C-extensions (e.g., `greenlet`, `sqlalchemy` speedups) under PyPy.
- **Dynamic Interpreter Selection:** The `Makefile` and `scripts/run.sh` must use CPython by default. PyPy selection must be triggered by an environment variable (e.g., `USE_PYPY=true`).
- **Environment Management:** Manage separate virtual environments (`.venv` for CPython and `.venv-pypy` for PyPy) using `uv`.

## Acceptance Criteria
- [ ] Dependency Audit: All current dependencies are confirmed compatible with PyPy 3.12.
- [ ] `make run` defaults to CPython.
- [ ] `make run USE_PYPY=true` activates the `.venv-pypy` environment.
- [ ] `scripts/run.sh` activations logic is updated and verified for both environments.
- [ ] Full `pytest` suite passes under both CPython and PyPy.
