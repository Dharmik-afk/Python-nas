# DEBUG.md — Project Debug Context
**Version:** 3.2.0
**Scope:** Py_server (Architecture 2.0)
**Target Agent:** Gemini CLI Agent

---

## 1. Known Bugs & Issues (CRITICAL)

### Bug: Copyparty Hashing Mismatch
- **Status:** **OPEN / WORKAROUND ACTIVE**
- **Symptom:** When `Hasher.get_copyparty_hash()` is enabled, login handshakes fail with `invalid password: '%x...'` even with correct credentials.
- **Root Cause:** Incompatibility between the Python implementation of the SHA-512 iteration loop and Copyparty's internal algorithm, or incorrect salt loading from `~/.config/copyparty/ah-salt.txt`.
- **Workaround:** Both `Hasher.get_copyparty_hash()` and `Hasher.get_internal_proxy_password()` currently return the **raw input** (Plain Text).
- **Security Impact:** Proxy traffic between FastAPI and Copyparty (port 8090) contains plain-text credentials. This is mitigated by Copyparty only listening on `127.0.0.1`.

### Issue: Health Check Shadowing
- **Status:** **FIXED**
- **Root Cause:** The catch-all route in `frontend_routes.py` was defined before the `/health` endpoint, causing health checks to return 307 redirects to `/login`.
- **Fix:** Moved `/health` endpoint definition above router inclusions in `app/main.py`.

---

## 2. Project Execution Model

### Language & Runtime Stack
- Python 3.12 (FastAPI)
- Jinja2 + HTMX + Alpine.js

### Architecture
- **Process 1:** FastAPI (Port 8000)
- **Process 2:** Copyparty (Port 8090, Internal Only)
- **Orchestrator:** `supervisor/supervisor.py`

### Entry Points
- `scripts/run.sh`: Main launcher.
- `scripts/manage.py`: User management CLI.
- `app/main.py`: FastAPI application.

---

## 3. Debugging Protocol

### Step 1: Check Supervisor Logs
```bash
tail -f logs/server.log
```
Look for `[Supervisor]` or `[Handshake]` prefixes.

### Step 2: Test Handshake Manually
If login fails, verify the internal proxy manually:
```bash
curl -u <user>:<pass> http://127.0.0.1:8090/?pmask
```

### Step 3: Database Verification
```bash
python3 scripts/manage.py list-users
```

---

## 4. Safety & Stability
- ✅ SQLite DB: `storage/db/server.db`
- ✅ Session Persistence: `storage/db/sessions.json`
- ✅ Internal Config: `copyparty/copyparty.conf` (Auto-generated)