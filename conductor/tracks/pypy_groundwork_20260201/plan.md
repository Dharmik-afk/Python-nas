# Implementation Plan: PyPy Groundwork

## Phase 1: Dependency Audit & PyPy Environment Setup [checkpoint: 52081f1]
**Goal:** Confirm runtime compatibility for all dependencies and establish the `.venv-pypy` environment.

- [x] Task: Audit dependencies for PyPy compatibility c67b3ea
    - [x] Generate a list of current dependencies from `pyproject.toml`.
    - [x] Verify PyPy 3.12 compatibility for key packages: `fastapi`, `pydantic`, `sqlalchemy` (check `greenlet` support), `uvicorn`, and `cffi`.
    - [x] Identify any packages requiring `clang` or native builds on Termux for PyPy.
    - [x] Document the audit findings in `audit_results.md`.
- [x] Task: Create and sync the PyPy virtual environment using uv d0d8dcc
    - [x] Check if `pypy3` is available on the system path.
    - [x] Initialize the environment: `uv venv --python pypy3.12 .venv-pypy`.
    - [x] Perform a full sync: `VIRTUAL_ENV=.venv-pypy uv sync`.
    - [x] Verify the installation by running `VIRTUAL_ENV=.venv-pypy python --version`.
    - *Note: Adapted to use `pip` and `requirements-pypy.txt` as `uv` failed to inspect PyPy on Termux. Also downgraded to PyPy 3.11.*
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Dependency Audit & PyPy Environment Setup' (Protocol in workflow.md)

## Phase 2: Dynamic Runtime Logic (Makefile & Scripts) [checkpoint: 52081f1]
**Goal:** Enable switching between `.venv` and `.venv-pypy` via the `USE_PYPY` flag.

- [x] Task: Write Tests: Verify `scripts/run.sh` environment activation logic 14761fe
    - [x] Create a standalone test script to simulate environment selection.
    - [x] Verify that `USE_PYPY=true` correctly identifies `.venv-pypy`.
    - [x] Verify that the default (no flag) correctly identifies `.venv`.
- [x] Task: Implement: Update `scripts/run.sh` to switch between runtimes 14761fe
    - [x] Modify the VENV activation logic in `scripts/run.sh` to use the `USE_PYPY` environment variable.
    - [x] Add a safety check to ensure the selected VENV exists before activation.
    - [x] Ensure `PYTHONPATH` and other variables are correctly inherited.
- [x] Task: Implement: Update `Makefile` to support `USE_PYPY` 14761fe
    - [x] Update `run`, `test`, and `manage` targets to pass the `USE_PYPY` variable.
    - [x] Add a `setup-pypy` target for one-command environment initialization.
    - [x] Update the `help` target to document the new `USE_PYPY=true` flag.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Dynamic Runtime Logic (Makefile & Scripts)' (Protocol in workflow.md) 14761fe
