# System Administrator Manual
**Project:** Python File Server (Architecture 2.0)
**Last Updated:** December 29, 2025

This manual documents the operational procedures for managing the single-port file server, including configuration, user management, and security protocols.

---

## 1. Quick Start

### Installation
Run the automated setup to create the uv environment (CPython), install dependencies, and initialize the database:
```bash
make setup
```

**High-Performance Mode (PyPy):**
The server is fully compatible with PyPy 3.11+, which offers significant performance improvements for media metadata processing and request routing while maintaining a lower memory footprint compared to standard CPython.
To set up the PyPy environment (requires `pypy3` installed):
```bash
make setup-pypy
```

### Starting the Server
Start the supervisor (manages both FastAPI and Copyparty):
```bash
make run
```

**Run with PyPy:**
To launch the server using the PyPy runtime:
```bash
USE_PYPY=true make run
```
- **Frontend (FastAPI):** http://<server-ip>:8000
- **Backend (Copyparty):** http://<server-ip>:8090 (if enabled in .env)

---

## 2. Configuration (`.env`)

The system relies on a `.env` file in the project root for configuration. This file is automatically loaded on startup.

| Variable | Default | Description |
| :--- | :--- | :--- |
| `FRONTEND_PORT` | 8000 | The public port for the main interface. |
| `FRONTEND_HOST` | 0.0.0.0 | Network binding (0.0.0.0 for LAN access). |
| `CUSTOM_SERVE_DIR` | (Empty) | **Critical:** The absolute path to the directory you want to stream. Defaults to `storage/files`. |
| `COPYPARTY_HOST` | 127.0.0.1 | Set to `0.0.0.0` to expose the backend UI for debugging. |
| `DEBUG` | False | Set to `True` for verbose logs and backend exposure. |
| `COPYPARTY_ADMIN_PASS`| (Generated)| The internal password for the `admin` proxy user. |

### Changing the Stream Directory
To change the folder being served (the "Jail Root"), you can use the helper command:
```bash
make set-dir dir=/path/to/your/media
```
This updates `CUSTOM_SERVE_DIR` in your `.env` file. Restart the server (`make run`) to apply.

---

## 3. User Management

User accounts are managed via the CLI. All changes are automatically synced to the backend.

| Action | Command | Description |
| :--- | :--- | :--- |
| **List Users** | `make list-users` | Shows ID, Username, and Permissions. |
| **Add User** | `make add-user user=<name>` | Creates a new user. Prompts for password. |
| **Add Admin** | `make add-user user=<name> perms=ADMIN` | Creates a user with full Read/Write/Admin rights. |
| **Delete User** | `make delete-user user=<name>` | Removes a user and revokes access. |
| **Change Password** | `make change-password user=<name>` | Updates credentials. |

**Permissions Reference:**
- `r` (Read-only): Can view and download.
- `rw` (Read-Write): Can upload and delete own files.
- `ADMIN` (Full): Can manage server and see all files.

---

## 4. Security Architecture

### The "Jail" (Stream Directory)
The server enforces a strict security boundary based on `CUSTOM_SERVE_DIR`.
- **Confinement:** Users **cannot** access files outside this directory (e.g., `../../secret`). attempts are logged and blocked (404 Not Found).
- **System Protection:** Critical system paths (Project Root, `/usr`, `/etc`) are explicitly restricted even if the jail is misconfigured.
- **Obfuscation:** Restricted paths return `404 Not Found` instead of `403 Forbidden` to hide their existence.

### Architecture 2.0
- **Supervisor:** A single entry point (`supervisor.py`) manages the lifecycle of the frontend and backend.
- **Proxy:** Users interact *only* with FastAPI (Port 8000). Requests are authenticated and then proxied to Copyparty (Port 8090) over a private loopback connection.
- **Copyparty UI:** By default, the Copyparty UI is hidden. If you need it for debugging, set `COPYPARTY_HOST=0.0.0.0` in `.env`.

---

## 5. Troubleshooting & Debugging

### Logs
- **Main Log:** `logs/server.log` (Contains startup info, access logs, and errors).
- **Console:** The `make run` command streams logs to stdout.

### Accessing the Backend UI
If you need to debug the underlying file engine:
1. Edit `.env` and set `COPYPARTY_HOST=0.0.0.0`.
2. Restart the server.
3. Access `http://<server-ip>:8090`.
4. Log in with the `COPYPARTY_ADMIN_USER` and `COPYPARTY_ADMIN_PASS` found in `.env` (or `app/core/config.py`).

### Common Issues
- **"File not found" on existing file:** Check if the file is outside `CUSTOM_SERVE_DIR`. The security jail is strict.
- **Upload fails:** Check permissions (`make list-users`). Guest users (`r`) cannot upload.
