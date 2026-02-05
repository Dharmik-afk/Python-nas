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
| File | Line | Purpose |
| :--- | :--- | :--- |
| `alembic/env.py` | 12 | Import `app` models/base. |
| `app/core/user_sync.py` | 8 | Import `scripts.manage`. |
| `app/tests/test_supervisor_interpreter.py` | 8 | Resolve project root for testing. |
| `scripts/manage.py` | 11 | Resolve project root for imports. |
| `scripts/verify_permissions.py` | 9 | Resolve project root for imports. |
| `supervisor/supervisor.py` | 12 | Import `app.core.config`. |

## 3. Notable Dependencies & Import Patterns
- **FastAPI Entry Point (`app/main.py`):** Uses absolute (`from app.core...`, `from app.backend...`) imports.
- **`app/core/` and `app/backend/`:** Standardized to absolute imports.
- **Supervisor (`supervisor/supervisor.py`):** Depends on `app.core.config`.
- **User Sync (`app/core/user_sync.py`):** Cross-imports from `scripts/manage.py`, creating a dependency from `app` to `scripts`.
- **Scripts:** Often depend on `app` modules for shared logic or configuration.

## 4. Potential Circular Dependencies (To Verify)
- `app.core.user_sync` <-> `scripts.manage` (Identified cross-import).
- `app.main` -> `app.backend.routes.api_routes` -> `app.core.auth` -> `app.main` (Check if auth depends on main).
