# Implementation Plan: Audit and Refactor Login Integration

This plan outlines the steps to refactor the authentication system for better integration with `copyparty`, including permission enforcement and dynamic UI adjustments.

## Phase 1: Hash Harmonization & Discovery [checkpoint: 1d1e7d5]
Goal: Fix the "Copyparty Hashing Mismatch" bug and ensure credentials are correctly hashed for proxying.

- [x] **Task 1: Audit Copyparty Hashing Algorithm**
    - [x] Sub-task: Analyze `copyparty` source or documentation to identify the exact SHA-512 iteration parameters.
    - [x] Sub-task: Create a standalone Python script to reproduce the mismatch reported in `DEBUG.md`.
- [x] **Task 2: Fix `Hasher.get_copyparty_hash()`**
    - [x] Sub-task: Write tests in `tests/test_security.py` that expect the correct hashed output for a known input.
    - [x] Sub-task: Implement the correct SHA-512 iteration loop in `app/core/security.py`.
    - [x] Sub-task: Update `Hasher.get_internal_proxy_password()` to use the new hashing logic.
- [x] **Task: Conductor - User Manual Verification 'Phase 1: Hash Harmonization & Discovery' (Protocol in workflow.md)****

## Phase 2: Permission Verification Engine
Goal: Implement the ability to query `copyparty` for user-specific permissions.

- [ ] **Task 1: Implement Permission Fetching in `copyparty_service.py`**
    - [ ] Sub-task: Write tests for a new method `get_user_permissions(username, password)`.
    - [ ] Sub-task: Implement `get_user_permissions` using `httpx` to query `copyparty`'s internal API or check its configuration.
- [ ] **Task 2: Update Authentication Flow**
    - [ ] Sub-task: Write tests for `app/backend/routes/auth_routes.py` to ensure permissions are fetched upon successful login.
    - [ ] Sub-task: Update the login route to store retrieved permissions in the `SessionManager` and the encrypted session cookie.
- [ ] **Task: Conductor - User Manual Verification 'Phase 2: Permission Verification Engine' (Protocol in workflow.md)**

## Phase 3: Dynamic UI Enforcement
Goal: Adjust the frontend UI based on the user's retrieved permissions.

- [ ] **Task 1: Expose Permissions to Jinja2 Templates**
    - [ ] Sub-task: Write tests ensuring the template context includes the user's permission set.
    - [ ] Sub-task: Update `app/core/templates.py` or add a context processor to make permissions globally available to templates.
- [ ] **Task 2: Conditional UI Rendering**
    - [ ] Sub-task: Update `app/frontend/templates/partials/file_browser_content.html` to hide/show action buttons (Upload, Create Folder, Delete) based on permissions.
    - [ ] Sub-task: Update the file browser route in `app/frontend/routes/frontend_routes.py` to filter available actions.
- [ ] **Task: Conductor - User Manual Verification 'Phase 3: Dynamic UI Enforcement' (Protocol in workflow.md)**

## Phase 4: Transparent Proxying & Session Sync
Goal: Finalize the session synchronization and ensure all proxied requests are correctly authenticated.

- [ ] **Task 1: Audit Proxy Header Propagation**
    - [ ] Sub-task: Write integration tests verifying that requests to `/api/raw/` contain the correct `Authorization` headers.
    - [ ] Sub-task: Refactor `app/backend/routes/download_routes.py` and `upload_routes.py` to use a centralized header generation helper.
- [ ] **Task 2: Final Session Persistence Audit**
    - [ ] Sub-task: Test login persistence across server restarts and browser refreshes.
    - [ ] Sub-task: Verify that session expiry in FastAPI triggers a corresponding logout or re-auth with `copyparty`.
- [ ] **Task: Conductor - User Manual Verification 'Phase 4: Transparent Proxying & Session Sync' (Protocol in workflow.md)**
