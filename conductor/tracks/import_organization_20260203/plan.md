# Implementation Plan - Internal Import & Dependency Organization

This plan outlines the steps to standardize internal imports, remove `sys.path` hacks, and ensure robust, package-native execution.

## Phase 1: Analysis & Initial Mapping [checkpoint: a4106f4]
Understand the current state of imports and dependencies.

- [x] Task: Generate Initial Dependency Map
    - [x] Analyze the codebase to identify current import patterns and dependencies.
    - [x] Create `conductor/dependency_map.md` documenting the initial state, including identified `sys.path` hacks and potential circular dependencies.
- [x] Task: Audit `sys.path` Usage
    - [x] Search for and list all occurrences of `sys.path.append`, `sys.path.insert`, and `PYTHONPATH` modifications in the codebase.
    - [x] Document these in the dependency map as targets for removal.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Analysis & Initial Mapping' (Protocol in workflow.md)

## Phase 2: Import Standardization (Core & Backend) [checkpoint: 5c0dd57]
Convert core modules to use absolute imports and remove path hacks.

- [x] Task: Refactor `app/core` Imports
    - [x] Convert all relative imports in `app/core` to absolute imports (e.g., `from app.core...`).
    - [x] Verify no circular dependencies are introduced.
- [x] Task: Refactor `app/backend` Imports
    - [x] Convert all relative imports in `app/backend` to absolute imports.
    - [x] Ensure `app/backend` modules correctly import from `app/core`.
- [x] Task: Update Dependency Map
    - [x] Update `conductor/dependency_map.md` to reflect the changes in `app/core` and `app/backend`.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Import Standardization (Core & Backend)' (Protocol in workflow.md)

## Phase 3: Entry Point & Script Refactoring [checkpoint: b990c9d]
Ensure entry points run as modules without path hacks.

- [x] Task: Refactor `main.py` (Root)
    - [x] Modify `main.py` (if applicable) or ensure it's redundant/correctly forwarding to `app.main`.
    - [x] Ensure it can be run via `python -m main` (if kept) or `uv run`.
- [x] Task: Refactor `supervisor/supervisor.py`
    - [x] Remove `sys.path` hacks.
    - [x] Ensure it runs via `python -m supervisor.supervisor`.
- [x] Task: Refactor `scripts/`
    - [x] specific scripts like `manage.py` to use absolute imports.
    - [x] Verify they run correctly from the project root.
- [x] Task: Update Dependency Map
    - [x] Update `conductor/dependency_map.md` to reflect entry point dependencies.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Entry Point & Script Refactoring' (Protocol in workflow.md)

## Phase 4: Frontend & Tests [checkpoint: 328d534]
Standardize frontend imports and ensure test suite compatibility.

- [x] Task: Refactor `app/frontend` Imports
    - [x] Convert all relative imports in `app/frontend` to absolute imports.
- [x] Task: Refactor Test Imports
    - [x] Update `app/tests` to use absolute imports for the application code.
    - [x] Remove any test-specific `sys.path` hacks.
- [x] Task: Verify Test Suite
    - [x] Run `pytest` from the project root and ensure all tests pass.
- [x] Task: Finalize Dependency Map
    - [x] Perform a final audit of the codebase.
    - [x] Complete `conductor/dependency_map.md` with the final, clean architecture.
- [x] Task: Conductor - User Manual Verification 'Phase 4: Frontend & Tests' (Protocol in workflow.md)
