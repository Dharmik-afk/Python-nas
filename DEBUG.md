# DEBUG.md — Project Debug Context
**Version:** 3.1.0
**Scope:** Py_server (FastAPI/HTMX Refactor)
**Target Agent:** Gemini CLI Agent

---

## Purpose of This File

This file defines **mandatory debugging protocols** for the Gemini CLI agent when working on this specific project.

**When active, this file overrides the agent's default debugging behavior.**

---

## 1. Project Execution Model (MANDATORY)

### Language & Runtime Stack

**Primary Language(s):**
- Python 3.11+ (FastAPI)
- HTML/CSS/JS (Jinja2, HTMX, Bootstrap 5)

**Execution Environment:**
- **Server:** Uvicorn (ASGI)
- **Framework:** FastAPI
- **Auth:** Session-based proxy to Copyparty
- **Process Manager:** `CopyPartyManager` (Internal Python Service)
- **Backend:** `copyparty` (Subprocess) configured via `data/copyparty.conf`

### Execution Architecture

**Control Flow Model:**
- **Asynchronous (Frontend):** FastAPI handles web requests, authenticates via session cookies, and proxies to the backend.
- **Subprocess (Backend):** `copyparty` runs on `127.0.0.1:8090`. It reads `data/copyparty.conf` for user accounts and volume permissions.
- **Metrics:** Real-time tracking in `backend/app/core/metrics.py`.

### Entry Points

1.  **Main Entry Point:** `run.sh --dir <path>`
2.  **FastAPI Entry:** `backend/app/main.py`
3.  **Test Suite:** `backend/tests/test_api.py` (Run with `pytest`)

---

## 2. Debugging Protocol

### Step 1: Verification via Tests
Before fixing, attempt to reproduce the issue using a test case:
```bash
cd backend && pytest
```

### Step 2: Check Logs & Config
1.  **FastAPI Logs:** `data/server.log`
2.  **Backend Logs:** `data/copyparty.log`
3.  **Metrics:** `data/metrics.json`
4.  **Backend Config:** Check `data/copyparty.conf` to ensure users and paths are configured correctly.

### Step 3: Auth Debugging
- If **Login Fails**: Check `server.log` for authentication proxy errors.
- If **Proxy Fails (403/401)**:
    - Verify `data/copyparty.conf` contains the expected password hash.
    - Check if `CopyPartyManager` was restarted after user changes (current limitation: requires restart).

---

## 3. Success Metrics & Success Criteria

**The project is considered "Healthy" when:**
- `pytest` returns all passes.
- `GET /api/v1/stats` returns valid JSON.
- `copyparty` process is active (Check `ps aux | grep copyparty`).
- `data/copyparty.conf` exists and is valid INI format.
- No "Connection Refused" errors in `server.log`.

---

## 4. Safety & Stability

- ❌ Never disable `validate_and_resolve_path`.
- ❌ Never hardcode paths; use `settings.SERVE_DIR`.
- ✅ Always use `StreamingResponse` for proxied files.
- ✅ Ensure `python-cryptography` is installed via `pkg` (Termux) or compiled correctly.
