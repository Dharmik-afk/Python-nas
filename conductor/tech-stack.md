# Technology Stack: Python FastAPI File Server

## Backend
*   **Programming Language:** Python 3.x
*   **Web Framework:** FastAPI (with Uvicorn as the ASGI server)
*   **Logic & Orchestration:** 
    *   Unified frontend architecture serving as a management layer.
    *   **Core Engine:** Deep integration with `copyparty` for file-serving operations, indexing, and management.
    *   **Process Management:** Supervisor model managing the FastAPI and `copyparty` subprocesses.

## Frontend
*   **Template Engine:** Jinja2 (Server-side rendering)
*   **UI Framework:** Bootstrap (CSS/Layout)
*   **Interactivity:** htmx (Providing dynamic, single-page application behavior)
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
*   **Execution:** `make` (via `Makefile`), `scripts/run.sh`.
*   **Package Management:** `requirements.txt`.
