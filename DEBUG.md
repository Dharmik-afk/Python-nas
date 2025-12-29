# DEBUG.md — Project Debug Context
**Version:** 3.3.0
**Scope:** Py_server (Architecture 2.0)
**Target Agent:** Gemini CLI Agent

---

## 1. Known Bugs & Issues (CRITICAL)

### Bug: Copyparty Hashing Mismatch
- **Status:** **OPEN / WORKAROUND ACTIVE**
- **Symptom:** When `Hasher.get_copyparty_hash()` is enabled, login handshakes fail with `invalid password: '%x...'` even with correct credentials.
- **Root Cause:** Incompatibility between the Python implementation of the SHA-512 iteration loop and Copyparty's internal algorithm.
- **Workaround:** Both `Hasher.get_copyparty_hash()` and `Hasher.get_internal_proxy_password()` currently return the **raw input** (Plain Text).
- **Security Impact:** Proxy traffic between FastAPI and Copyparty (port 8090) contains plain-text credentials. This is mitigated by Copyparty normally listening only on `127.0.0.1`.

### Issue: Health Check Shadowing
- **Status:** **FIXED**
- **Fix:** Moved `/health` endpoint definition above router inclusions in `app/main.py`.

---

## 2. Project Execution Model

### Language & Runtime Stack
- Python 3.12 (FastAPI)
- Jinja2 + HTMX + Alpine.js
- **Config**: `python-dotenv` loads settings from `.env`.

### Architecture
- **Process 1:** FastAPI (Port 8000)
- **Process 2:** Copyparty (Port 8090).
    - **Prod**: Binds to `127.0.0.1` (Hidden).
    - **Debug**: Binds to `0.0.0.0` (Visible) if `COPYPARTY_HOST=0.0.0.0` in `.env`.
- **Orchestrator:** `supervisor/supervisor.py`

### Entry Points
- `scripts/run.sh`: Main launcher (loads `.env`).
- `scripts/manage.py`: User management CLI.
- `app/main.py`: FastAPI application.

---

## 3. Debugging Protocol

### Step 1: Check Supervisor Logs
```bash
tail -f logs/server.log
```

### Step 2: Debugging Backend UI
To bypass FastAPI and access Copyparty directly:
1. Edit `.env`: Set `COPYPARTY_HOST=0.0.0.0` and `DEBUG=True`.
2. Restart: `make run`.
3. Browse: `http://<server-ip>:8090`.
4. Login: Use `COPYPARTY_ADMIN_USER` / `COPYPARTY_ADMIN_PASS` from `.env`.

### Step 3: Database Verification
```bash
python3 scripts/manage.py list-users
```

---

## 4. Safety & Stability
- ✅ **Jail Confinement**: `CUSTOM_SERVE_DIR` in `.env` limits file access.
- ✅ **Path Obfuscation**: Restricted paths return `404 Not Found`.
- ✅ SQLite DB: `storage/db/server.db`
- ✅ Session Persistence: `storage/db/sessions.json`
- ✅ Internal Config: `copyparty/copyparty.conf` (Auto-generated)
