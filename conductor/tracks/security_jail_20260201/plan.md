# Implementation Plan - Path Validation Refinement & Startup Security Enforcement

This plan focuses on enforcing a strict jail around the active `SERVE_DIR` and implementing a fail-fast startup check in the `Settings` class to prevent insecure configurations.

## Phase 1: Foundation & Startup Security (Fail-Fast) [checkpoint: daf915a]
Focus on the Pydantic `Settings` class to ensure the server cannot start with an insecure `SERVE_DIR`.

- [x] **Task: Write Tests for Settings Validation in `app/tests/test_security.py`** 3152f68
- [x] **Task: Implement Fail-Fast Validation in `app/core/config.py`** 3152f68
- [x] **Task: Verify Settings Security** 3152f68
- [x] **Task: Conductor - User Manual Verification 'Phase 1: Foundation & Startup Security' (Protocol in workflow.md)** daf915a

## Phase 2: Strict Runtime Jail Enforcement [checkpoint: ac60cb5]
Update the core path validation logic to strictly isolate the active `SERVE_DIR`.

- [x] **Task: Write Tests for Strict Jail Isolation in `app/tests/test_security.py`** 4befa7d
    - [x] Append tests to `app/tests/test_security.py`.
    - [x] Test: `validate_and_resolve_path` allows access within `CUSTOM_SERVE_DIR`.
    - [x] Test: `validate_and_resolve_path` raises `404` for paths inside the default `storage/files` when a `CUSTOM_SERVE_DIR` is active (even if `storage/files` is in `ALLOWED_OVERRIDE_DIRS`).
    - [x] Test: `validate_and_resolve_path` raises `404` for any path outside the active `SERVE_DIR`.
- [x] **Task: Refactor `validate_and_resolve_path` in `app/core/file_security.py`** 4befa7d
    - [x] Simplify the logic to prioritize the `base_dir` (which is passed as the active `SERVE_DIR`) as the absolute boundary.
    - [x_ Ensure that `full_path.is_relative_to(resolved_base_dir)` is the primary and final arbiter of access.
    - [x] Remove any logic that might allow "leaking" into other allowed override directories if they are not the *current* `base_dir`.
- [x] **Task: Verify Runtime Isolation** 4befa7d
    - [x] Run tests: `pytest app/tests/test_security.py`
    - [x] Run existing security tests to ensure no regressions.
- [x] **Task: Conductor - User Manual Verification 'Phase 2: Strict Runtime Jail Enforcement' (Protocol in workflow.md)** ac60cb5

## Phase 3: Integration & Regression Testing [checkpoint: 64290c0]
Ensure the changes work correctly across all routes and don't break existing functionality.

- [x] **Task: Comprehensive Security Regression** f91d287
    - [x] Run all project tests: `pytest`
    - [x] Specifically verify `app/tests/test_api.py` and `app/tests/test_mobile_api.py` with both default and custom directory configurations.
- [x] **Task: Documentation Update** 83f74ea
    - [x] Update `ADMIN_MANUAL.md` or `DEBUG.md` to explain the new fail-fast behavior and the strict jail isolation.
- [x] **Task: Conductor - User Manual Verification 'Phase 3: Integration & Regression' (Protocol in workflow.md)** bc7f911
