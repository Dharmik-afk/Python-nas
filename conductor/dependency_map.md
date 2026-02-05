# Initial Dependency Map

This document maps the project's dependency structure and identifies `sys.path` hacks.

## 1. Project Structure (High-Level)
- `app/`: Main FastAPI application.
    - `core/`: Shared logic, configuration, and security.
    - `backend/`: API routes, services, and database models.
    - `frontend/`: UI routes, templates, and static files.
- `supervisor/`: Process management (Uvicorn + Copyparty).
- `scripts/`: Management and utility scripts.
- `copyparty/`: Configuration for the storage engine.
- `alembic/`: Database migrations.

## 2. Identified `sys.path` Hacks
| File | Line | Purpose | Status |
| :--- | :--- | :--- | :--- |
| `alembic/env.py` | 12 | Import `app` models/base. | Removed |
| `app/core/user_sync.py` | 8 | Import `scripts.manage`. | Removed |
| `app/tests/test_supervisor_interpreter.py` | 8 | Resolve project root for testing. | To Remove in Ph 4 |
| `scripts/manage.py` | 11 | Resolve project root for imports. | Removed |
| `scripts/verify_permissions.py` | 9 | Resolve project root for imports. | Removed |
| `supervisor/supervisor.py` | 12 | Import `app.core.config`. | Removed |

## 3. Notable Dependencies & Import Patterns
- **FastAPI Entry Point (`app/main.py`):** Uses absolute (`from app.core...`, `from app.backend...`) imports.
- **Supervisor (`supervisor/supervisor.py`):** Runs as a module (`python -m supervisor.supervisor`). Absolute imports.
- **Scripts:** Run as modules (e.g., `python -m scripts.manage`). Absolute imports.
- **User Sync (`app/core/user_sync.py`):** Uses absolute import for `scripts.manage`.

## 4. Potential Circular Dependencies (To Verify)
- `app.core.user_sync` <-> `scripts.manage` (Identified cross-import).
- `app.main` -> `app.backend.routes.api_routes` -> `app.core.auth` -> `app.main` (Check if auth depends on main).
