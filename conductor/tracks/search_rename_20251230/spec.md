# Track Specification: Search, Rename, and Hash Fix

## Overview
This track addresses a critical authentication bug and expands the file management capabilities of the FastAPI File Server. It focuses on aligning the hashing algorithm with `copyparty`, adding a global file search, and enabling file/folder renaming.

## Functional Requirements
*   **Hashing Alignment:** Fix the `Hasher.get_copyparty_hash()` method to correctly match Copyparty's SHA-512 iteration loop, removing the current plain-text workaround.
*   **File Search:** Implement a search bar in the UI that allows users to find files and folders recursively starting from their current directory.
*   **Renaming:** Enable users with 'write' permissions to rename files and folders directly from the file browser.

## Technical Requirements
*   **Backend (Python):**
    *   Implement correct SHA-512 iteration in `app/core/security.py`.
    *   Add `/api/v1/fs/search` endpoint proxying to Copyparty's search API.
    *   Add `/api/v1/fs/rename` endpoint proxying to Copyparty's move/rename API.
*   **Frontend (HTMX + Jinja2):**
    *   Add a search input field in `file_browser.html`.
    *   Add a "Rename" button/modal in the file card overlay.
    *   Update UI to reflect permission masks for the rename action.

## Acceptance Criteria
*   Login handshakes succeed with `get_copyparty_hash()` enabled (verified against a real Copyparty instance or known hash).
*   Users can search for files and see results rendered in the file list.
*   Users can rename files/folders and see the updated names immediately.
*   Permission checks correctly disable renaming for read-only users.
