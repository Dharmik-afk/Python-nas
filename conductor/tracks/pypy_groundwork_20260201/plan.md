# Implementation Plan: PyPy Groundwork

## Phase 1: Dependency Audit & PyPy Environment Setup
**Goal:** Confirm runtime compatibility for all dependencies and establish the `.venv-pypy` environment.

- [ ] Task: Audit dependencies for PyPy compatibility
    - [ ] Generate a list of current dependencies from `pyproject.toml`.
    - [ ] Verify PyPy 3.12 compatibility for key packages: `fastapi`, `pydantic`, `sqlalchemy` (check `greenlet` support), `uvicorn`, and `cffi`.
    - [ ] Identify any packages requiring `clang` or native builds on Termux for PyPy.
    - [ ] Document the audit findings in `DEBUG.md`.
- [ ] Task: Create and sync the PyPy virtual environment using `uv`
    - [ ] Check if `pypy3` is available on the system path.
    - [ ] Initialize the environment: `uv venv --python pypy3.12 .venv-pypy`.
    - [ ] Perform a full sync: `VIRTUAL_ENV=.venv-pypy uv sync`.
    - [ ] Verify the installation by running `VIRTUAL_ENV=.venv-pypy python --version`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Dependency Audit & PyPy Environment Setup' (Protocol in workflow.md)

## Phase 2: Dynamic Runtime Logic (Makefile & Scripts)
**Goal:** Enable switching between `.venv` and `.venv-pypy` via the `USE_PYPY` flag.

- [ ] Task: Write Tests: Verify `scripts/run.sh` environment activation logic
    - [ ] Create a standalone test script to simulate environment selection.
    - [ ] Verify that `USE_PYPY=true` correctly identifies `.venv-pypy`.
    - [ ] Verify that the default (no flag) correctly identifies `.venv`.
- [ ] Task: Implement: Update `scripts/run.sh` to switch between runtimes
    - [ ] Modify the VENV activation logic in `scripts/run.sh` to use the `USE_PYPY` environment variable.
    - [ ] Add a safety check to ensure the selected VENV exists before activation.
    - [ ] Ensure `PYTHONPATH` and other variables are correctly inherited.
- [ ] Task: Implement: Update `Makefile` to support `USE_PYPY`
    - [ ] Update `run`, `test`, and `manage` targets to pass the `USE_PYPY` variable.
    - [ ] Add a `setup-pypy` target for one-command environment initialization.
    - [ ] Update the `help` target to document the new `USE_PYPY=true` flag.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Dynamic Runtime Logic (Makefile & Scripts)' (Protocol in workflow.md)
