# Implementation Plan - Path Validation Refinement & Startup Security Enforcement

This plan focuses on enforcing a strict jail around the active `SERVE_DIR` and implementing a fail-fast startup check in the `Settings` class to prevent insecure configurations.

## Phase 1: Foundation & Startup Security (Fail-Fast)
Focus on the Pydantic `Settings` class to ensure the server cannot start with an insecure `SERVE_DIR`.

- [ ] **Task: Write Tests for Settings Validation in `app/tests/test_security.py`**
    - [ ] Append tests to `app/tests/test_security.py`.
    - [ ] Test: `Settings` initializes successfully with a default safe path (`storage/files`).
    - [ ] Test: `Settings` initializes successfully with a custom path outside the project root.
    - [ ] Test: `Settings` raises `ValueError` if `CUSTOM_SERVE_DIR` is set to the project root (restricted) without an override.
    - [ ] Test: `Settings` initializes successfully if a restricted path is explicitly added to `ALLOWED_OVERRIDE_DIRS`.
- [ ] **Task: Implement Fail-Fast Validation in `app/core/config.py`**
    - [ ] Add a `@root_validator` to the `Settings` class.
    - [ ] Implement logic to check if `self.SERVE_DIR` is within any `RESTRICTED_DIRS`.
    - [ ] If restricted, verify it is also in `ALLOWED_OVERRIDE_DIRS`.
    - [ ] Raise `ValueError` if the security check fails.
- [ ] **Task: Verify Settings Security**
    - [ ] Run tests: `pytest app/tests/test_security.py`
    - [ ] Verify that the server fails to start when `.env` is intentionally misconfigured.
- [ ] **Task: Conductor - User Manual Verification 'Phase 1: Foundation & Startup Security' (Protocol in workflow.md)**

## Phase 2: Strict Runtime Jail Enforcement
Update the core path validation logic to strictly isolate the active `SERVE_DIR`.

- [ ] **Task: Write Tests for Strict Jail Isolation in `app/tests/test_security.py`**
    - [ ] Append tests to `app/tests/test_security.py`.
    - [ ] Test: `validate_and_resolve_path` allows access within `CUSTOM_SERVE_DIR`.
    - [ ] Test: `validate_and_resolve_path` raises `404` for paths inside the default `storage/files` when a `CUSTOM_SERVE_DIR` is active (even if `storage/files` is in `ALLOWED_OVERRIDE_DIRS`).
    - [ ] Test: `validate_and_resolve_path` raises `404` for any path outside the active `SERVE_DIR`.
- [ ] **Task: Refactor `validate_and_resolve_path` in `app/core/file_security.py`**
    - [ ] Simplify the logic to prioritize the `base_dir` (which is passed as the active `SERVE_DIR`) as the absolute boundary.
    - [ ] Ensure that `full_path.is_relative_to(resolved_base_dir)` is the primary and final arbiter of access.
    - [ ] Remove any logic that might allow "leaking" into other allowed override directories if they are not the *current* `base_dir`.
- [ ] **Task: Verify Runtime Isolation**
    - [ ] Run tests: `pytest app/tests/test_security.py`
    - [ ] Run existing security tests to ensure no regressions.
- [ ] **Task: Conductor - User Manual Verification 'Phase 2: Strict Runtime Jail Enforcement' (Protocol in workflow.md)**

## Phase 3: Integration & Regression Testing
Ensure the changes work correctly across all routes and don't break existing functionality.

- [ ] **Task: Comprehensive Security Regression**
    - [ ] Run all project tests: `pytest`
    - [ ] Specifically verify `app/tests/test_api.py` and `app/tests/test_mobile_api.py` with both default and custom directory configurations.
- [ ] **Task: Documentation Update**
    - [ ] Update `ADMIN_MANUAL.md` or `DEBUG.md` to explain the new fail-fast behavior and the strict jail isolation.
- [ ] **Task: Conductor - User Manual Verification 'Phase 3: Integration & Regression' (Protocol in workflow.md)**
