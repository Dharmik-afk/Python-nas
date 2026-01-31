# Specification: Integrate `uv` into Infrastructure

## Overview
This track involves a comprehensive migration from the legacy `pip` and `venv` management system to `uv`. The goal is to leverage `uv` for faster environment setup, deterministic dependency management via `uv.lock`, and simplified execution using `uv run`.

## Functional Requirements
1.  **Dependency Migration:**
    -   Convert existing `requirements.txt` into a modern `pyproject.toml` configuration.
    -   Generate a `uv.lock` file to ensure reproducible builds.
2.  **Environment Management:**
    -   Update system setup scripts to install `uv` automatically.
    -   Use `uv` to create and manage the virtual environment (replacing standard `python -m venv`).
3.  **Command & Script Refactoring:**
    -   **Makefile:** Update all Python-related targets (e.g., `setup`, `run`, `lint`, `test`) to utilize `uv run` or `uv pip`.
    -   **Setup Scripts:** Update `scripts/setup_system.sh` to handle `uv` installation (via `pkg install uv` on Termux) and environment initialization.
    -   **Supervisor:** Modify `supervisor/supervisor.py` to execute subprocesses (FastAPI, etc.) using `uv run` for consistent environment handling.

## Non-Functional Requirements
-   **Performance:** Significantly reduce the time required for `make setup`.
-   **Reliability:** Ensure 100% parity in runtime behavior between the legacy and `uv`-managed environments.

## Acceptance Criteria
-   `make setup` successfully installs `uv`, creates a virtual environment, and installs all dependencies from `pyproject.toml`.
-   `make run` successfully launches the supervisor and all services using `uv run`.
-   The system successfully passes all existing tests when executed via `uv run pytest`.
-   The `requirements.txt` file is no longer used as the source of truth for dependencies.

## Out of Scope
-   Migration of non-Python dependencies (system packages).
-   Updates to GitHub Actions or CI/CD pipelines (focused on local/server infrastructure).
