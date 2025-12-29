# Gemini CLI Agent — Project Context
Version: 2.2.0 (Architecture 2.0 + Jail Security)

## Agent Identity
- Name: gemini-cli-agent
- Role: Codebase Operational Auditor & Developer
- Focus: Architecture 2.0 (Single-Port, Supervisor-Driven)

## Architecture 2.0 OverView
The system has been consolidated into a single public-facing port (8000) using a Supervisor model, with strict filesystem confinement.

### 1. Process Orchestration
- **Supervisor (`supervisor/supervisor.py`)**: Manages two subprocesses:
    - **FastAPI (8000)**: Public frontend and proxy.
    - **Copyparty (8090)**: Internal file engine. Configurable host via `.env` (Default: `127.0.0.1`, Debug: `0.0.0.0`).
- **Health Monitoring**: Supervisor performs HTTP health checks on FastAPI and restarts either process if they exit unexpectedly.

### 2. Unified Security & Confinement
- **Jail Security (`app/core/file_security.py`)**:
    - **Serve Directory**: Strictly confined to `CUSTOM_SERVE_DIR` (from `.env`).
    - **Path Traversal**: All requests are validated against the absolute serve path. Sibling/parent access is blocked.
    - **Obfuscation**: Restricted or non-existent paths return `404 Not Found` to hide system structure.
    - **Restricted Paths**: Explicitly blocks Project Root and System Directories (`/usr`, `/etc`) even if the jail is misconfigured.
- **Hasher Class**: Centralized singleton for `sha256_crypt` and JWT.
- **Session Manager**: Persists encrypted proxy credentials in `storage/db/sessions.json`.

### 3. User & Config Management
- **Configuration**: Driven by `.env` file (using `python-dotenv`).
    - **Key Settings**: `CUSTOM_SERVE_DIR`, `COPYPARTY_HOST`, `DEBUG`.
- **Centralized CLI (`scripts/manage.py`)**: Unified tool for user management and config syncing.
- **Documentation**: See `ADMIN_MANUAL.md` for operational details.

### 4. Integration State
- **FastAPI Handshake**: Every login performs a real-time verification handshake with Copyparty.
- **Single-Source-of-Truth**: All user data resides in SQLite (`storage/db/server.db`).

## Execution Protocol
1.  **Configure**: Edit `.env` or run `make set-dir dir=/path/to/media`.
2.  **Run**: `make run` (triggers `scripts/run.sh`).
3.  **Logs**: Centralized in `logs/server.log`.

## Active Extensions
- project-inspector (Manages DEBUG.md)
- python-dev (Standard Python rules)
- workflow-safety (Shell execution policies)