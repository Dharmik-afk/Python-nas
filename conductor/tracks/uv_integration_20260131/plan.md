# Implementation Plan: Integrate `uv` into Infrastructure

This plan outlines the steps to migrate the project's Python dependency and environment management from `pip`/`venv` to `uv`, adopting a modern `pyproject.toml` and `uv.lock` workflow.

## Phase 1: Dependency Migration
- [x] Task: Initialize `pyproject.toml` and `uv.lock` 97faa51
    - [x] Create `pyproject.toml` based on current `requirements.txt`
    - [x] Generate `uv.lock` using `uv lock`
    - [x] Verify dependency resolution with `uv sync`
- [x] Task: Conductor - User Manual Verification 'Phase 1: Dependency Migration' (Protocol in workflow.md) 97faa51

## Phase 2: Infrastructure Updates
- [x] Task: Update `scripts/setup_system.sh` 2fa81ad
    - [x] Add logic to install `uv` (using `pkg install uv` for Termux compatibility)
    - [x] Replace `python3 -m venv` with `uv venv`
    - [x] Replace `pip install` with `uv pip install` or `uv sync`
- [x] Task: Refactor `Makefile` 2fa81ad
    - [x] Update `setup` target to use `uv` for environment and dependency setup
    - [x] Update `run` target to use `uv run`
    - [x] Update `test`, `lint`, and other Python targets to use `uv run`
- [x] Task: Conductor - User Manual Verification 'Phase 2: Infrastructure Updates' (Protocol in workflow.md) 2fa81ad

## Phase 3: Service Orchestration Update
- [x] Task: Modify `supervisor/supervisor.py` 22e613f
    - [x] Update command generation to prepend `uv run` or use the `uv` managed python executable
    - [x] Ensure subprocesses inherit the `uv` environment correctly
- [x] Task: Conductor - User Manual Verification 'Phase 3: Service Orchestration Update' (Protocol in workflow.md) 22e613f

## Phase 4: Verification and Finalization
- [x] Task: Full System Integration Test bdb8791
    - [x] Execute `make setup` in a fresh environment
    - [x] Run all tests via `uv run pytest`
    - [x] Verify `make run` starts the system correctly
- [x] Task: Cleanup Legacy Files bdb8791
    - [x] Mark `requirements.txt` as deprecated or remove it
    - [x] Update `README.md` and `ADMIN_MANUAL.md` to reflect `uv` usage
- [x] Task: Conductor - User Manual Verification 'Phase 4: Verification and Finalization' (Protocol in workflow.md) bdb8791
