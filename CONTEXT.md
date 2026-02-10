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
*Summary and link to be added after audit.*

### [alembic/](./alembic/.context.md)
*Summary and link to be added after audit.*

### [scripts/](./scripts/.context.md)
*Summary and link to be added after audit.*

### [supervisor/](./supervisor/.context.md)
*Summary and link to be added after audit.*
