# Specification: AI Context Hierarchy (v1.0)

## Overview
Transform the monolithic `GEMINI.md` context into a hierarchical, scoped system to improve maintainability, reduce token pollution, and provide agents with task-specific instructions. This introduces a "Nearest-First" resolution order where local context overrides or supplements global context.

## Functional Requirements
1.  **Context Resolution Protocol**:
    - Update root `GEMINI.md` to define the "Context Loading Protocol".
    - Agents must search for `.context.md` files starting from the current working directory upwards to the project root.
    - Priority: Nearest `.context.md` > Parent `.context.md` > Root `GEMINI.md`.
2.  **Centralized Overlays**:
    - Create a `.context/` directory at the project root for cross-cutting concerns (e.g., `security.md`, `auth.md`, `performance.md`).
3.  **Directory-Based Scoping**:
    - Implement initial `.context.md` files for the following real paths:
        - `app/backend/` (FastAPI/SQLAlchemy specifics)
        - `app/frontend/` (HTMX/Alpine.js/Jinja2 specifics)
        - `app/tests/` (Testing patterns and coverage requirements)
        - `scripts/` (Maintenance and automation specifics)
4.  **Context Loader Tool (`scripts/context_loader.py`)**:
    - Develop a Python utility to aggregate context.
    - Features:
        - `--path`: Specify directory to resolve context for.
        - `--task`: Optional hint to include specific role overlays.
        - Output: Merged Markdown with clear headers indicating source files.
5.  **Root Integrity**:
    - Preserve core identity, global safety invariants, and operational guidelines in the root `GEMINI.md`.

## Acceptance Criteria
- [ ] `GEMINI.md` contains the documented "Context Loading Protocol".
- [ ] `scripts/context_loader.py` successfully merges root context with nested `.context.md` files.
- [ ] `.context/` folder exists with a `security.md` overlay.
- [ ] Verified `.context.md` files exist in `app/backend/`, `app/frontend/`, `app/tests/`, and `scripts/`.
