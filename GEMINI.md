# Gemini CLI Agent — Project Context
Version: 2.4.0 (Architecture 2.0 + Media Preview V3)

## Agent Identity
- Name: gemini-cli-agent
- Role: Codebase Operational Auditor & Developer
- Focus: Architecture 2.0 (Single-Port, Supervisor-Driven)

## 1. Project Overview
- **Core Goal**: A high-performance, Termux-native file server and media streamer.
- **Architecture**: Single-port (8000) unified gateway. All traffic (UI, API, Files) passes through FastAPI, which proxies to an internal Copyparty instance (8090).
- **Process Management**: A Python-based `supervisor/supervisor.py` manages the lifecycles of both FastAPI (Uvicorn) and Copyparty.

## 2. Technology Stack
- **Backend**: Python 3.12 (FastAPI), Pydantic (Settings), SQLAlchemy (SQLite), Alembic (Migrations).
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
- **Google Photos Aesthetic**: Minimalist split layout, floating details popover, and permission-aware management (Rename/Delete/Upload).

## 6. Security & Jail Confinement
- **Jail Root**: Configured via `CUSTOM_SERVE_DIR` in `.env`. Defaults to `storage/files`.
- **Confinement**: Path validation ensures no access outside the jail. Critical paths (`/usr`, `/etc`, Project Root) are blocked.
- **Obfuscation**: Restricted paths return `404 Not Found` to prevent discovery.
- **Session Persistence**: `storage/db/sessions.json` manages user sessions across restarts.

## 7. Client-Server Communication
The application employs a hybrid communication model designed for responsiveness and efficiency:
- **HTMX (Hypermedia-Driven)**: Primary engine for navigation and partial UI updates.
  - **Navigation**: Directory browsing uses `hx-get` on file cards to fetch and swap the `#main-content` container.
  - **Search**: Real-time filtering via `hx-get="/api/v1/fs/search/ui"` triggered by `keyup changed delay:500ms`.
  - **CRUD Operations**: Deletion (`hx-delete`) and Upload (`hx-post` with `multipart/form-data`) use HTMX to update the file grid without full page reloads.
  - **Toasts**: Server-side events are broadcasted to the frontend using the `HX-Trigger` header, which Alpine.js listens for to display toast notifications.
- **Alpine.js (Reactive State)**: Handles complex client-side interactions.
  - **Lightbox**: Manages the media previewer state, gesture handling, and fetches gallery metadata via `fetch()` from `/api/v1/gallery/`.
  - **Modals/Prompts**: Custom rename/mkdir workflows use `htmx.ajax()` triggered by Alpine.js `@click` events after user confirmation.
- **Service Worker (`sw.js`)**: Acts as a client-side proxy. Intercepts `Range` requests for video streaming to provide a smooth, buffer-less experience.

## 8. API Ecosystem
The backend exposes a structured versioned API (`/api/v1`) for both the internal UI and external clients:

### Authentication (`/api/v1/auth`)
- `POST /login`: Session-based login for browsers. Sets `access_token` and `session_id` cookies.
- `POST /token`: OAuth2-compatible Bearer token endpoint for CLI/Mobile clients.
- `POST /logout`: Clears session and cookies.

### File System (`/api/v1/fs`)
- `GET /fs/search/ui`: Returns rendered HTML partials for search results or directory listings.
- `POST /fs/rename/{path}`: Renames a file/folder. Requires 'm' (move) permission.
- `POST /fs/mkdir/{path}`: Creates a new directory. Requires 'w' (write) permission.
- `DELETE /fs/{path}`: Deletes a resource. Requires 'd' (delete) permission.

### Media & Streaming
- `GET /download/{path}`: The primary gateway for file access. Proxies to Copyparty.
  - **Thumbnails**: Supports `?thumb=WxH` for dynamic image/video thumbnail generation.
  - **Streaming**: Supports standard HTTP Range requests for video seeking.
- `POST /upload/{path}`: Handles `multipart/form-data` uploads, proxying bytes directly to the storage engine.
- `GET /api/v1/gallery/{path}`: Returns JSON metadata (names, URLs, types) of all media in a directory for the Lightbox component.

## 9. Operational Workflow
- **Setup**: `make setup` (System pkgs, Venv, Pip, DB Init, Default Admin).
- **Run**: `make run` (Triggers `scripts/run.sh` which launches the supervisor).
- **Set Directory**: `make set-dir dir=/path/to/media` to update the jail root.
- **User Management**: `make add-user user=name`, `make list-users`, `make delete-user user=name`.

## Active Extensions
- **project-inspector**: Manages technical details in `DEBUG.md`.
- **python-dev**: Standard Python development, debugging, and env management.
- **workflow-safety**: Enforcement of shell execution policies and destructive operation warnings.
- **conductor**: Orchestrates multi-step project tracks (plans in `conductor/archive/` or `conductor/tracks/`).
