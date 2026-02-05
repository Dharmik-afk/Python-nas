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

## Phase 3: Entry Point & Script Refactoring
Ensure entry points run as modules without path hacks.

- [ ] Task: Refactor `main.py` (Root)
    - [ ] Modify `main.py` (if applicable) or ensure it's redundant/correctly forwarding to `app.main`.
    - [ ] Ensure it can be run via `python -m main` (if kept) or `uv run`.
- [ ] Task: Refactor `supervisor/supervisor.py`
    - [ ] Remove `sys.path` hacks.
    - [ ] Ensure it runs via `python -m supervisor.supervisor`.
- [ ] Task: Refactor `scripts/`
    - [ ] specific scripts like `manage.py` to use absolute imports.
    - [ ] Verify they run correctly from the project root.
- [ ] Task: Update Dependency Map
    - [ ] Update `conductor/dependency_map.md` to reflect entry point dependencies.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Entry Point & Script Refactoring' (Protocol in workflow.md)

## Phase 4: Frontend & Tests
Standardize frontend imports and ensure test suite compatibility.

- [ ] Task: Refactor `app/frontend` Imports
    - [ ] Convert all relative imports in `app/frontend` to absolute imports.
- [ ] Task: Refactor Test Imports
    - [ ] Update `app/tests` to use absolute imports for the application code.
    - [ ] Remove any test-specific `sys.path` hacks.
- [ ] Task: Verify Test Suite
    - [ ] Run `pytest` from the project root and ensure all tests pass.
- [ ] Task: Finalize Dependency Map
    - [ ] Perform a final audit of the codebase.
    - [ ] Complete `conductor/dependency_map.md` with the final, clean architecture.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Frontend & Tests' (Protocol in workflow.md)
