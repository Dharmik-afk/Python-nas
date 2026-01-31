# Implementation Plan: Integrate `uv` into Infrastructure

This plan outlines the steps to migrate the project's Python dependency and environment management from `pip`/`venv` to `uv`, adopting a modern `pyproject.toml` and `uv.lock` workflow.

## Phase 1: Dependency Migration
- [ ] Task: Initialize `pyproject.toml` and `uv.lock`
    - [ ] Create `pyproject.toml` based on current `requirements.txt`
    - [ ] Generate `uv.lock` using `uv lock`
    - [ ] Verify dependency resolution with `uv sync`
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Dependency Migration' (Protocol in workflow.md)

## Phase 2: Infrastructure Updates
- [ ] Task: Update `scripts/setup_system.sh`
    - [ ] Add logic to install `uv` (using `pkg install uv` for Termux compatibility)
    - [ ] Replace `python3 -m venv` with `uv venv`
    - [ ] Replace `pip install` with `uv pip install` or `uv sync`
- [ ] Task: Refactor `Makefile`
    - [ ] Update `setup` target to use `uv` for environment and dependency setup
    - [ ] Update `run` target to use `uv run`
    - [ ] Update `test`, `lint`, and other Python targets to use `uv run`
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Infrastructure Updates' (Protocol in workflow.md)

## Phase 3: Service Orchestration Update
- [ ] Task: Modify `supervisor/supervisor.py`
    - [ ] Update command generation to prepend `uv run` or use the `uv` managed python executable
    - [ ] Ensure subprocesses inherit the `uv` environment correctly
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Service Orchestration Update' (Protocol in workflow.md)

## Phase 4: Verification and Finalization
- [ ] Task: Full System Integration Test
    - [ ] Execute `make setup` in a fresh environment
    - [ ] Run all tests via `uv run pytest`
    - [ ] Verify `make run` starts the system correctly
- [ ] Task: Cleanup Legacy Files
    - [ ] Mark `requirements.txt` as deprecated or remove it
    - [ ] Update `README.md` and `ADMIN_MANUAL.md` to reflect `uv` usage
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Verification and Finalization' (Protocol in workflow.md)
