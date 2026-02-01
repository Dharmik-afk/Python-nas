# Technology Stack: Python FastAPI File Server

## Backend
*   **Programming Language:** Python 3.x (CPython 3.12, PyPy 3.11+ (High-Performance Mode))
*   **Web Framework:** FastAPI (with Uvicorn as the ASGI server)
*   **Logic & Orchestration:** 
    *   Unified frontend architecture serving as a management layer.
    *   **Core Engine:** Deep integration with `copyparty` for file-serving operations, indexing, and management.
    *   **Process Management:** Supervisor model managing the FastAPI and `copyparty` subprocesses.
    *   **Mobile API:** JSON-based REST API with Pydantic response modeling and JWT security.

## Frontend
*   **Template Engine:** Jinja2 (Server-side rendering)
*   **UI Framework:** Bootstrap (CSS/Layout)
*   **Interactivity:** HTMX (AJAX/Partial updates) and Alpine.js (Client-side state)
*   **Media:** Artplayer.js (Video playback and gestures)
*   **Icons:** Custom SVG icon set and Bootstrap Icons.

## Database & Persistence
*   **Database:** SQLite (for user accounts, session persistence, and metadata)
*   **ORM:** SQLAlchemy
*   **Migrations:** Alembic

## Security & Authentication
*   **Unified Auth:** 
    *   Hybrid authentication system utilizing `passlib` (SHA-512/SHA-256) and `python-jose` (JWT).
    *   **Copyparty Integration:** The login system is partially derived from or integrated with `copyparty`'s authentication mechanisms to ensure seamless proxying and access control.
*   **Dependencies:** `python-multipart`, `requests`, `httpx`.

## Infrastructure & Tooling
*   **Execution:** `make` (via `Makefile`), `scripts/run.sh`. Supports dynamic runtime switching via `USE_PYPY=true`.
*   **Package Management:** `uv` (`pyproject.toml`, `uv.lock`).
*   **AI Context Management:** Hierarchical context system (scoped `.context.md` files) with `scripts/context_loader.py` for agent orchestration.

## Mobile Client App (Groundwork)
*   **Framework:** React Native (Expo Managed Workflow)
*   **Language:** TypeScript
*   **State Management:** Zustand (with persistence)
*   **Navigation:** React Navigation (Stack)
*   **List Rendering:** @shopify/flash-list
*   **Media Playback:** expo-av
