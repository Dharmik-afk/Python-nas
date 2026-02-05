# Specification - Internal Import & Dependency Organization

This track focuses on standardizing the internal import structure of the project, removing legacy `sys.path` hacks, ensuring robust, package-native execution, and documenting the resulting architecture.

## 1. Overview
Currently, the project uses inconsistent import styles and relies on manual `sys.path` manipulations to resolve modules. This track will refactor the codebase to use absolute imports and leverage standard Python package discovery. A dependency tree will be generated at the start to map the current state and will be updated iteratively to reflect the improved structure.

## 2. Functional Requirements
- **Initial Dependency Mapping:** Analyze the codebase at the beginning of the track and generate an initial dependency map (e.g., `conductor/dependency_map.md`) to document the current state of imports and relationships.
- **Standardize Imports:** Convert all internal imports to the absolute format (e.g., `from app.core import config`).
- **Remove Path Hacks:** Identify and remove all instances of `sys.path.append`, `sys.path.insert`, and similar manipulations used to resolve internal modules.
- **Package-Native Execution:** Configure and verify that all entry points (e.g., `app/main.py`, `supervisor/supervisor.py`, `scripts/manage.py`) function correctly when run as modules (e.g., `python -m app.main` or `uv run`).
- **Resolve Circularities:** Identify and resolve any circular dependency loops that are currently masked by import hacks.
- **Fix Test Resolution:** Ensure the test suite (`pytest`) correctly discovers and imports modules from the project root without manual path intervention.
- **Iterative Map Updates:** Update the `conductor/dependency_map.md` file throughout the process to reflect the standardized structure.

## 3. Non-Functional Requirements
- **Zero Behavioral Change:** The refactor must not alter the application's external functionality or performance.
- **Maintainability:** Standardized imports should make it easier for new developers (and AI agents) to navigate the codebase.

## 4. Acceptance Criteria
- [ ] An initial dependency map is created in Phase 1.
- [ ] No `sys.path` modifications for internal imports exist in the codebase.
- [ ] All internal imports follow the `from app...` or `import app...` absolute pattern.
- [ ] The application starts and runs successfully via `python -m app.main`.
- [ ] The supervisor starts and manages processes correctly via `python -m supervisor.supervisor`.
- [ ] All tests pass using `pytest` from the project root.
- [ ] No circular import errors are present during startup or test execution.
- [ ] The `conductor/dependency_map.md` file is up-to-date and accurately reflects the final, clean architecture.

## 5. Out of Scope
- Major restructuring of the directory hierarchy (beyond minor moves if essential for package discovery).
- Modification of external library versions in `pyproject.toml` (unless required for PEP 517/518 compliance).
