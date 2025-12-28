# Gemini CLI Agent — Project Context
Version: 2.1.0 (Architecture 2.0)

## Agent Identity
- Name: gemini-cli-agent
- Role: Codebase Operational Auditor & Developer
- Focus: Architecture 2.0 (Single-Port, Supervisor-Driven)

## Architecture 2.0 OverView
The system has been consolidated into a single public-facing port (8000) using a Supervisor model.

### 1. Process Orchestration
- **Supervisor (`supervisor/supervisor.py`)**: Manages two subprocesses:
    - **FastAPI (8000)**: Public frontend and proxy.
    - **Copyparty (8090)**: Private internal file engine (bound to `127.0.0.1`).
- **Health Monitoring**: Supervisor performs HTTP health checks on FastAPI and restarts either process if they exit unexpectedly.

### 2. Unified Security & Hashing
- **Hasher Class (`app/core/security.py`)**: A centralized singleton (`hasher`) for all cryptographic needs.
    - **DB Hashing**: Standard `sha256_crypt` via `passlib`.
    - **JWT Management**: Encapsulated token generation.
    - **Proxy Credentials**: Currently using **Plain-Text** for Copyparty proxying (see DEBUG.md for known bug regarding hash mismatches).
- **Session Manager**: Persists encrypted proxy credentials in `storage/db/sessions.json`.

### 3. User Management
- **Centralized CLI (`scripts/manage.py`)**: Unified tool for:
    - Adding/Deleting users.
    - Changing passwords.
    - Syncing the database to `copyparty/copyparty.conf`.
- **Config Sync**: The `app.core.user_sync` module is now a thin wrapper around `manage.py` logic.

### 4. Integration State
- **FastAPI Handshake**: Every login now performs a real-time verification handshake with Copyparty before granting access.
- **Single-Source-of-Truth**: All user data resides in SQLite (`storage/db/server.db`).

## Execution Protocol
1.  **Run**: `make run` (triggers `scripts/run.sh`).
2.  **Setup**: `make setup` (rebuilds venv and DB).
3.  **Logs**: Centralized in `logs/server.log`.

## Active Extensions
- project-inspector (Manages DEBUG.md)
- python-dev (Standard Python rules)
- workflow-safety (Shell execution policies)
