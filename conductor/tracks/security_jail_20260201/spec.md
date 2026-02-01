# Track Specification: Path Validation Refinement & Startup Security Enforcement

## Overview
This track strengthens the server's security by enforcing a strict "jail" around the active serve directory (`SERVE_DIR`). It ensures that once a serve directory is set (default or custom), NO file access is permitted outside of it, even if the requested path is otherwise considered "safe" or "allowed" in the global configuration. It also introduces a "fail-fast" startup check.

## Functional Requirements
1.  **Strict Jail Enforcement (Runtime):**
    -   The `validate_and_resolve_path` function MUST resolve all requests relative to the active `settings.SERVE_DIR`.
    -   **Rule:** If a resolved path is NOT relative to the current `SERVE_DIR`, the server MUST return `404 Not Found`.
    -   **Isolation:** This rule applies even if the out-of-bounds path is listed in `ALLOWED_OVERRIDE_DIRS`. The `SERVE_DIR` is the only valid root for the current session.

2.  **Startup Security Check (Fail-Fast):**
    -   The `Settings` class (via Pydantic validation) MUST verify the `SERVE_DIR` upon initialization.
    -   **Rule:** If `SERVE_DIR` is within a `RESTRICTED_DIRS` path (e.g., the project root), it MUST be explicitly listed in `ALLOWED_OVERRIDE_DIRS`.
    -   **Action:** If this condition is not met, the application MUST raise an error and exit immediately, preventing the server from running in an insecure state.

3.  **Global vs. Local Security:**
    -   `RESTRICTED_DIRS` and `ALLOWED_OVERRIDE_DIRS` are used *only* to validate whether a path is eligible to become the `SERVE_DIR`.
    -   Once `SERVE_DIR` is validated and active, it becomes the absolute boundary.

## Non-Functional Requirements
-   **Security:** Prevents "leakage" where a user might access the default `storage/files` while a custom directory is active, or vice-versa.
-   **Clarity:** Provides clear, immediate feedback (shutdown) if the server environment is misconfigured.

## Acceptance Criteria
-   [ ] Server fails to start if `SERVE_DIR` is restricted and not overridden.
-   [ ] `validate_and_resolve_path` returns `404 Not Found` for any access attempt outside the active `SERVE_DIR`.
-   [ ] If `CUSTOM_SERVE_DIR` is set to `/mnt/usb`, attempts to access `storage/files` (even if it's an "allowed override") return `404 Not Found`.
-   [ ] Automated tests confirm that changing `SERVE_DIR` correctly shifts the security boundary.

## Out of Scope
-   Automated creation of custom directories.
-   UI-based editing of the `.env` file (handled by `Makefile` or manual edits).
