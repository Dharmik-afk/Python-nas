Python File Server: Authoritative Context
Architecture: Clean Single-Port (Termux-Optimized, Supervisor-Driven)

Version: 2.0 (Optimized for Storage & UI Snappiness)

1. Core Design Goals
Termux Native: Run reliably in Android userland without root, Docker, or systemd.

Unified Gateway: Expose exactly one TCP port (8000). All traffic (UI, API, Files) passes through FastAPI.

Python-Centric: Use Python for both the web layer and the process supervision layer.

Resource Efficient: Optimize for low RAM and abrupt process termination by Android.

Storage-First: Maintain a clear boundary between application logic and user data.

2. Revised Project Structure
Plaintext

fileserver/
├── app/                        # Application Logic
│   ├── core/                   # Shared Infrastructure
│   │   ├── config.py           # Environment & App Settings
│   │   ├── logger.py           # Unified logging (FastAPI + Supervisor)
│   │   └── security.py         # Path validation & Auth helpers
│   ├── frontend/               # UI Layer
│   │   ├── routes/             # Page rendering routes
│   │   ├── static/             # CSS/JS (Alpine.js / HTMX)
│   │   └── templates/          # Jinja2 (Subdivided for HTMX)
│   │       ├── layouts/        # Base HTML skeletons
│   │       ├── pages/          # Full page views
│   │       └── partials/       # HTMX fragments for partial swaps
│   └── backend/                # API Layer
│       ├── routes/             # API endpoints
│       ├── services/           # Copyparty proxy (Streaming logic)
│       └── models/             # Pydantic schemas
│
├── storage/                    # Persistent Data Root
│   ├── files/                  # Actual user-uploaded content
│   ├── cache/                  # Thumbnails and ZIP temp files
│   └── db/                     # Metadata/Session DBs (if any)
│
├── supervisor/                 # Process Management
│   ├── supervisor.py           # The "Master" process manager
│   └── state.py                # Health tracking & status API
│
├── copyparty/                  # Storage Engine
│   └── copyparty.conf          # Internal localhost config
│
├── logs/                       # Rotating runtime logs
├── scripts/                    # Termux setup/utility scripts
├── Makefile                    # Task runner (setup, start, stop, logs)
└── .env                        # Environment variables
3. Component Model
A. The Python Supervisor
The "Master" process. It is the first script to run and is responsible for:

Spawning Copyparty as a subprocess bound to 127.0.0.1.

Spawning the FastAPI application (Uvicorn).

Performing health checks: Polling the FastAPI /health endpoint and Copyparty status.

Restarting failed components without killing the entire session.

B. FastAPI Gateway (Port 8000)
Frontend: Uses HTMX to swap partials/ into layouts/, providing a SPA-like feel without a heavy JS build step.

Backend: Acts as a reverse proxy for Copyparty.

Streaming: All file transfers MUST use StreamingResponse to bridge Copyparty and the Client, ensuring the Python process doesn't exceed Termux memory limits.

C. Copyparty (Internal)
Provides the heavy lifting for file indexing, thumbnails, and user permissions.

Constraint: Must never be reachable from the network; it only talks to the FastAPI services/ layer.

4. Operational Rules
Direct Action: All human interaction happens via the Makefile (e.g., make start, make setup).

Streaming Only: Do not load file bytes into memory. Use buffers.

Path Safety: Every path request from the UI must be scrubbed against the storage/files/ root in core/security.py.

Logging: All components must write to the /logs directory for centralized debugging via make logs.

Would you like me to generate the initial supervisor/supervisor.py or the app/core/config.py to get this structure started?
