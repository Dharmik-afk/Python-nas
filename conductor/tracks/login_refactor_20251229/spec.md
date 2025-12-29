# Track Specification: Audit and Refactor Login Integration

## Overview
This track aims to refine the hybrid authentication system between the FastAPI frontend and the internal `copyparty` engine. The primary goal is to ensure robust session management, transparent credential proxying, and strict permission enforcement derived from `copyparty`.

## Functional Requirements
*   **Transparent Proxying:** Implement a mechanism where FastAPI seamlessly passes authentication credentials or session tokens to `copyparty` without requiring additional user intervention or secondary login prompts.
*   **Permission Verification:** Upon login, the system MUST query `copyparty` to verify the user's credentials and retrieve their specific permissions/access rights.
*   **Dynamic UI Adaptation:** The user interface (buttons, functions, visible directories) must be dynamically rendered based on the permissions returned by `copyparty`. Users should only see options they are authorized to use.
*   **Session State Synchronization:** Ensure that the user's login state is consistent across both the FastAPI web interface and the proxied `copyparty` file services.
*   **Hash Harmonization:** Audit and update the credential hashing mechanism to ensure compatibility between the systems, resolving any "hash mismatch" errors.

## Acceptance Criteria
*   Users can log in via the FastAPI frontend and immediately access all file browser features managed by `copyparty`.
*   The system successfully queries `copyparty` for user permissions upon login.
*   The UI correctly hides/shows features (e.g., upload buttons, delete options) based on the user's retrieved permissions.
*   Authentication headers are correctly propagated to all proxied requests.
*   The "hash mismatch" errors reported in `DEBUG.md` are resolved.
*   All existing unit tests for authentication pass, and new tests cover the refactored logic.

## Out of Scope
*   Adding new user roles or complex permission hierarchies (we are only enforcing existing `copyparty` roles).
*   Major UI/UX redesign of the login pages (to be handled in a separate track).
