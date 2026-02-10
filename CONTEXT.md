# Project Context: python-nas

This file provides a centralized overview of the project's architecture, infrastructure, and core components. It serves as a primary entry point for understanding the codebase, specifically focusing on root-level files and aggregating context from sub-directories.

## Root Infrastructure and Configuration

### `main.py`
- **Purpose:** Entry point for the application. Currently simple, but intended to initialize and run the main service.
- **Key Symbols:**
    - `main()`: The primary execution function.
- **Dependencies:** None (Standard Library).

### `Makefile`
- **Purpose:** Orchestrates common development, build, and management tasks.
- **Key Symbols/Targets:**
    - `setup`: Performs a full system reset and fresh installation.
    - `install`: Initializes the Python environment and dependencies using `uv`.
    - `db-init`: Runs database migrations using `alembic`.
    - `run`: Starts the application via `scripts/run.sh`.
    - `test`: Executes the test suite using `pytest`.
    - `list-users`, `add-user`, `delete-user`: Manage application users.
- **Dependencies:** `scripts/setup_system.sh`, `scripts/run.sh`, `scripts/manage.py`, `uv`, `alembic`, `pytest`.

### `package.json`
- **Purpose:** Manages JavaScript-related development tools.
- **Key Symbols:**
    - `devDependencies`: Includes `prettier` for code formatting.
- **Dependencies:** `prettier`.

### `pyproject.toml`
- **Purpose:** Centralized configuration for the Python project, including metadata and dependencies.
- **Key Symbols:**
    - `[project]`: Defines name, version, and requirements.
    - `dependencies`: Lists all required Python libraries (FastAPI, SQLAlchemy, Alembic, etc.).
    - `[tool.uv]`: Configures the `uv` dependency manager.
- **Dependencies:** `uv`.

### `alembic.ini`
- **Purpose:** Configuration file for Alembic, the database migration tool.
- **Key Symbols:**
    - `script_location`: Points to the `alembic/` directory.
    - `sqlalchemy.url`: Database connection string placeholder (overridden in `app/core/config.py`).
- **Dependencies:** `alembic`.

### `README.md`
- **Purpose:** General project introduction, architectural overview, and quick-start guide.
- **Key Information:**
    - Project Goal: Lightweight Python-based file server.
    - Tech Stack: FastAPI, Copyparty, SQLAlchemy, Jinja2, HTMX.
    - Setup: `make setup` (CPython) or `make setup-pypy` (PyPy).
- **Dependencies:** None.

### `ADMIN_MANUAL.md`
- **Purpose:** Comprehensive guide for system administrators managing the server.
- **Key Information:**
    - Operations: Detailed setup, run, and user management commands.
    - Configuration: Explanation of `.env` variables (ports, host, `CUSTOM_SERVE_DIR`).
    - Security: Details on "Jail" confinement, fail-fast startup, and runtime isolation.
    - Troubleshooting: Log locations (`logs/server.log`) and backend UI debugging.
- **Dependencies:** None.

### `DEBUG.md`
- **Purpose:** Technical log of resolved bugs, known issues, and debugging protocols.
- **Key Information:**
    - History: Records fixes for Copyparty hashing, PyPy compatibility, and route resolution.
    - Known Issues: `uv` libc detection on Termux (workaround provided).
    - Execution Model: Process management via `supervisor/supervisor.py`.
    - Context System: Explains the hierarchical context loader (`scripts/context_loader.py`).
- **Dependencies:** None.

### `open_server.sh`
- **Purpose:** A small Android/Termux utility to open the server URL in the system's browser.
- **Key Symbols:**
    - `am start`: Android command to launch an intent for the server URL.
- **Dependencies:** Android OS.

---

## Application Structure

### [app/](./app/.context.md)
The main application package. Contains the FastAPI initialization (`main.py`) and serves as the container for backend, frontend, and core logic.

### [app/core/](./app/core/.context.md)
The engine of the application. Handles configuration (`Settings`), security (jail enforcement, path validation), authentication (JWT, sessions), and core utilities. Key modules include `file_security.py` for path validation and `session_manager.py` for persistent user sessions.

### [app/backend/](./app/backend/.context.md)
The core business logic layer. Contains database models, Pydantic schemas, and the implementation of the Mobile API and file management routes.

#### [app/backend/database/](./app/backend/database/.context.md)
SQLAlchemy-based database layer. Manages the `User` model and standard CRUD operations.

#### [app/backend/models/](./app/backend/models/.context.md)
Pydantic schemas used for API request/response validation (`FSItem`, `UserCreate`).

#### [app/backend/routes/](./app/backend/routes/.context.md)
FastAPI routers defining endpoints for `api`, `auth`, `download`, and `upload`.

#### [app/backend/services/](./app/backend/services/.context.md)
Service layer for interacting with Copyparty. Handles proxying of streams, uploads, and search requests.

### [app/frontend/](./app/frontend/.context.md)
The presentation layer of the application. Uses Jinja2 for server-side rendering, enhanced with HTMX and Alpine.js for a modern, reactive user experience.

#### [app/frontend/routes/](./app/frontend/routes/.context.md)
Frontend page controllers. Handles routing for browsing, login, and test pages.

#### [app/frontend/static/](./app/frontend/static/.context.md)
Client-side assets. Includes `sw.js` (Service Worker) for media caching and `style.css` for the glassmorphism UI.

#### [app/frontend/templates/](./app/frontend/templates/.context.md)
Jinja2 templates organized into `layouts`, `pages`, and `partials`. Key partials include `lightbox.html` for media viewing.

### [app/tests/](./app/tests/.context.md)
The automated test suite. Uses `pytest` to validate security jails, API endpoints, and frontend template logic. Employs extensive mocking to isolate the application from the physical filesystem and internal services.

### [alembic/](./alembic/.context.md)

### [scripts/](./scripts/.context.md)
*Summary and link to be added after audit.*

### [supervisor/](./supervisor/.context.md)
*Summary and link to be added after audit.*
