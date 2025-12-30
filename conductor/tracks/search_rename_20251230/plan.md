# Implementation Plan: Search, Rename, and Hash Fix

This plan details the steps to resolve the hashing mismatch and implement search/rename features.

## Phase 1: Authentication Hashing Resolution [checkpoint: 32224c0]
Goal: Align the internal hashing with Copyparty to secure the proxy connection.

- [x] **Task 1: Implement Correct SHA-512 Iteration** [24da13f]
    - [ ] Sub-task: Write a unit test in `app/tests/test_security.py` using a known Copyparty hash/password pair.
    - [ ] Sub-task: Update `Hasher.get_copyparty_hash` in `app/core/security.py` with the correct iteration logic.
    - [ ] Sub-task: Remove the plain-text workaround in `Hasher.get_internal_proxy_password`.
- [x] **Task: Conductor - User Manual Verification 'Phase 1: Authentication Hashing Resolution' (Protocol in workflow.md)** [32224c0]

## Phase 2: File Search Functionality [checkpoint: f678caa]
Goal: Add recursive file search to the file browser.

- [x] **Task 1: Backend Search Proxy** [a6e1a05]
    - [x] Sub-task: Write integration tests for the search endpoint.
    - [x] Sub-task: Implement `search_files` in `copyparty_service.py`.
    - [x] Sub-task: Add `/api/v1/fs/search` route in `api_routes.py`.
- [x] **Task 2: Frontend Search UI** [30cf2bc]
    - [x] Sub-task: Add a search bar to `app/frontend/templates/pages/file_browser.html`.
    - [x] Sub-task: Use HTMX to trigger searches and swap the `#file-list` content.
- [x] **Task: Conductor - User Manual Verification 'Phase 2: File Search Functionality' (Protocol in workflow.md)** [f678caa]

## Phase 3: File and Folder Renaming [checkpoint: 52cde52]
Goal: Allow users to rename items within the browser.

- [x] **Task 1: Backend Rename Proxy** [5a1ac61]
    - [x] Sub-task: Write integration tests for renaming files and directories.
    - [x] Sub-task: Implement `rename_item` in `copyparty_service.py` (using Copyparty's `move` API).
    - [x] Sub-task: Add `/api/v1/fs/rename` route in `api_routes.py`.
- [x] **Task 2: Frontend Rename UI** [c7e2245]
    - [x] Sub-task: Add a rename button to the action overlay in `app/frontend/templates/partials/file_browser_content.html`.
    - [x] Sub-task: Implement a simple rename prompt or modal using Alpine.js or vanilla JS.
- [x] **Task: Conductor - User Manual Verification 'Phase 3: File and Folder Renaming' (Protocol in workflow.md)** [52cde52]

## Phase 4: Login Regression Fix [checkpoint: b80d980]
Goal: Fix login failures caused by hash mismatch (SHA-256 vs SHA-512).

- [x] **Task 1: Reproduce and Fix Hash Verification** [64a7acb]
    - [x] Sub-task: Create a reproduction test case in `app/tests/test_auth_routes.py` with a legacy SHA-256 hash.
    - [x] Sub-task: Update `app/core/security.py` or `auth_routes.py` to correctly verify legacy hashes.
    - [x] Sub-task: Verify that new users (SHA-512) and old users (SHA-256) can both login.
- [x] **Task: Conductor - User Manual Verification 'Phase 4: Login Regression Fix' (Protocol in workflow.md)** [64a7acb]
