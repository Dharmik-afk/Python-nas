# Implementation Plan: Search, Rename, and Hash Fix

This plan details the steps to resolve the hashing mismatch and implement search/rename features.

## Phase 1: Authentication Hashing Resolution [checkpoint: 32224c0]
Goal: Align the internal hashing with Copyparty to secure the proxy connection.

- [x] **Task 1: Implement Correct SHA-512 Iteration** [24da13f]
    - [ ] Sub-task: Write a unit test in `app/tests/test_security.py` using a known Copyparty hash/password pair.
    - [ ] Sub-task: Update `Hasher.get_copyparty_hash` in `app/core/security.py` with the correct iteration logic.
    - [ ] Sub-task: Remove the plain-text workaround in `Hasher.get_internal_proxy_password`.
- [x] **Task: Conductor - User Manual Verification 'Phase 1: Authentication Hashing Resolution' (Protocol in workflow.md)** [32224c0]

## Phase 2: File Search Functionality
Goal: Add recursive file search to the file browser.

- [ ] **Task 1: Backend Search Proxy**
    - [ ] Sub-task: Write integration tests for the search endpoint.
    - [ ] Sub-task: Implement `search_files` in `copyparty_service.py`.
    - [ ] Sub-task: Add `/api/v1/fs/search` route in `api_routes.py`.
- [ ] **Task 2: Frontend Search UI**
    - [ ] Sub-task: Add a search bar to `app/frontend/templates/pages/file_browser.html`.
    - [ ] Sub-task: Use HTMX to trigger searches and swap the `#file-list` content.
- [ ] **Task: Conductor - User Manual Verification 'Phase 2: File Search Functionality' (Protocol in workflow.md)**

## Phase 3: File and Folder Renaming
Goal: Allow users to rename items within the browser.

- [ ] **Task 1: Backend Rename Proxy**
    - [ ] Sub-task: Write integration tests for renaming files and directories.
    - [ ] Sub-task: Implement `rename_item` in `copyparty_service.py` (using Copyparty's `move` API).
    - [ ] Sub-task: Add `/api/v1/fs/rename` route in `api_routes.py`.
- [ ] **Task 2: Frontend Rename UI**
    - [ ] Sub-task: Add a rename button to the action overlay in `app/frontend/templates/partials/file_browser_content.html`.
    - [ ] Sub-task: Implement a simple rename prompt or modal using Alpine.js or vanilla JS.
- [ ] **Task: Conductor - User Manual Verification 'Phase 3: File and Folder Renaming' (Protocol in workflow.md)**
