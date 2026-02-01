# Gemini CLI Agent — Project Context
Version: 2.5.0 (Architecture 2.0 + Hierarchical Context)

## Agent Identity
- Name: gemini-cli-agent
- Role: Codebase Operational Auditor & Developer
- Focus: Architecture 2.0 (Single-Port, Supervisor-Driven)

## 1. Project Overview
- **Core Goal**: A high-performance, Termux-native file server and media streamer.
- **Architecture**: Single-port (8000) unified gateway. All traffic (UI, API, Files) passes through FastAPI, which proxies to an internal Copyparty instance (8090).
- **Process Management**: A Python-based `supervisor/supervisor.py` manages the lifecycles of both FastAPI (Uvicorn) and Copyparty.

## 2. Technology Stack
- **Backend**: Python 3.x (CPython 3.12, PyPy 3.11+), FastAPI, Pydantic (Settings), SQLAlchemy (SQLite), Alembic (Migrations).
- **Frontend**: Jinja2 Templates, HTMX (Partial Swaps), Alpine.js (UI State/Interactions), Bootstrap CSS + Icons.
- **Media Engine**: Copyparty (Indexing, Thumbnails, Range Requests), custom `sw.js` (Service Worker) for zero-loading streaming and caching.
- **Process Control**: Supervisor (Python `subprocess`), Makefile (Task Runner).

## 3. Architecture 2.0 (Supervisor-Driven)
- **FastAPI (Port 8000)**: The only public-facing port. Handles Auth, UI rendering, and API requests.
- **Copyparty (Port 8090)**: Internal storage engine. Binds to `127.0.0.1` by default. Accessed via FastAPI's `services/copyparty_service.py`.
- **Health Checks**: Supervisor polls `/health` on FastAPI to ensure system stability.
- **Unified Logging**: All logs are centralized in `logs/server.log`.

## 4. Integration State
- **FastAPI Handshake**: Real-time verification handshake with Copyparty for logins.
- **Single-Source-of-Truth**: All user data resides in SQLite (`storage/db/server.db`).
- **User Sync**: `scripts/manage.py` and `app/core/user_sync.py` ensure credentials are mirrored between FastAPI and Copyparty.

## 5. Advanced Media Preview (V3)
- **High-Performance Lightbox**: Mobile-optimized gallery using Alpine.js for complex gesture handling (zoom, swipe).
- **Service Worker (`sw.js`)**: Intercepts media requests for persistent caching and "zero-loading" video streaming via Range Request interception.
- **MX Player Inspired Controls**: Vertical swipes for volume/brightness, double-tap skip, and intelligent auto-hiding playback controls in the video player.

## 6. Security & Jail Confinement
- **Jail Root**: Configured via `CUSTOM_SERVE_DIR` in `.env`. Defaults to `storage/files`.
- **Confinement**: Path validation ensures no access outside the jail. Critical paths (`/usr`, `/etc`, Project Root) are blocked.
- **Obfuscation**: Restricted paths return `404 Not Found` to prevent discovery.
- **Session Persistence**: `storage/db/sessions.json` manages user sessions across restarts.

## 7. Operational Workflow
- **Setup**: `make setup` (Default CPython) or `make setup-pypy` (PyPy 3.11+).
- **Run**: `make run` (Triggers `scripts/run.sh`). Use `USE_PYPY=true make run` for PyPy.
- **Set Directory**: `make set-dir dir=/path/to/media` to update the jail root.
- **User Management**: `make add-user user=name`, `make list-users`, `make delete-user user=name`.

## Active Extensions
- **project-inspector**: Manages technical details in `DEBUG.md`.
- **python-dev**: Standard Python development, debugging, and env management.
- **workflow-safety**: Enforcement of shell execution policies and destructive operation warnings.
- **conductor**: Orchestrates multi-step project tracks (plans in `conductor/archive/` or `conductor/tracks/`).

## 8. Context Loading Protocol

This project uses a hierarchical context system to manage agent instructions.



**Protocol:**

1.  **Search**: Upon starting a task in a directory, the agent MUST look for a `.context.md` file in the current directory and all parent directories up to the project root.

2.  **Resolution**: The agent MUST prioritize instructions in the *nearest* `.context.md` file (local scope) over those in parent files.

3.  **Aggregation**: The agent SHOULD read all relevant `.context.md` files to build a complete picture, applying the priority rule for conflicts.

4.  **Overlays**: If a `.context.md` file references a role overlay (e.g., `.context/security.md`), the agent MUST read that overlay.



## 9. Companion Apps

- **ClientApp (Android)**: A standalone React Native (Expo) application located in `ClientApp/`. It has its own isolated git repository and `GEMINI.md` context. It consumes the main server's Mobile API.
