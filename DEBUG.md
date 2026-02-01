# DEBUG.md — Project Debug Context
**Version:** 3.5.0
**Scope:** Py_server (Architecture 2.0)
**Target Agent:** Gemini CLI Agent

---

## 1. Resolved Issues (FIXED)

### Bug: Copyparty Hashing Mismatch
- **Status:** **FIXED**
- **Fix:** Implemented custom SHA-512 "sha2" algorithm compatible with Copyparty. Added salted proxy authentication (`internal_pw = username + password`) to prevent hash collisions for users with identical passwords.
- **Verification:** Handshake successful on both CPython and PyPy.

### Issue: PyPy 3.11 + Cryptography on Termux
- **Status:** **FIXED**
- **Workaround:** `app/core/auth.py` uses a custom `PurePythonCrypter` (HMAC-SHA256 + SHA256 stream cipher) when the binary `cryptography` library is missing. Verified robust session encryption across all runtimes.

### Issue: PyPy Handshake Timeout / Latency
- **Status:** **FIXED**
- **Symptom:** Login failed with `502 Bad Gateway` on PyPy due to 5s timeout.
- **Fix:** Increased handshake timeout to 15s and permission retrieval to 10s to accommodate PyPy JIT warm-up and mobile hardware latency.

### Issue: Root Path Resolution in Copyparty Proxy
- **Status:** **FIXED**
- **Symptom:** Root directory listed as `/.?pmask` (incorrect) instead of `/?pmask`.
- **Fix:** Refactored `_get_proxy_url` to correctly handle `.` as an empty path string.

### Issue: logger Import Failure in app/core/auth.py
- **Status:** **FIXED**
- **Fix:** Replaced incorrect import with `logging.getLogger(__name__)`.

### Issue: Health Check Shadowing
- **Status:** **FIXED**
- **Fix:** Moved `/health` endpoint definition above router inclusions in `app/main.py`.

---

## 2. Known Issues & Workarounds

### Issue: uv + PyPy Libc Detection
- **Status:** **WORKAROUND ACTIVE**
- **Symptom:** `uv venv` or `uv sync` fails with `Could not detect a glibc or a musl libc` when targeting PyPy.
- **Workaround:** Use `pypy3 -m venv` for environment creation and `pip install -r requirements-pypy.txt` (exported via `uv export`) for dependency management in the PyPy environment.

---

## 3. Project Execution Model

### Language & Runtime Stack
- Python 3.12 (FastAPI / CPython)
- PyPy 3.11+ (High-Performance Mode via `USE_PYPY=true`)
- Jinja2 + HTMX + Alpine.js
- **Config**: `python-dotenv` loads settings from `.env`.

### Architecture
- **Process 1:** FastAPI (Port 8000)
- **Process 2:** Copyparty (Port 8090).
    - **Prod**: Binds to `127.0.0.1` (Hidden).
    - **Debug**: Binds to `0.0.0.0` (Visible) if `COPYPARTY_HOST=0.0.0.0` in `.env`.
- **Orchestrator:** `supervisor/supervisor.py` (Interpreter-aware)

### Entry Points
- `scripts/run.sh`: Main launcher (loads `.env`).
- `scripts/manage.py`: User management CLI.
- `app/main.py`: FastAPI application.

---

## 4. Debugging Protocol

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

## 5. Safety & Stability
- ✅ **Jail Confinement**: `CUSTOM_SERVE_DIR` in `.env` limits file access.
- ✅ **Path Obfuscation**: Restricted paths return `404 Not Found`.
- ✅ SQLite DB: `storage/db/server.db`
- ✅ Session Persistence: `storage/db/sessions.json`
- ✅ Internal Config: `copyparty/copyparty.conf` (Auto-generated)

---

## 6. Context Hierarchy (Scoped AI Instructions)

### Maintenance
- **Root Context**: Global invariants and project identity are defined in `GEMINI.md`.
- **Scoped Contexts**: Directory-specific rules are defined in `.context.md` files (e.g., `app/backend/.context.md`).
- **Role Overlays**: Cross-cutting concerns go into `.context/*.md` (e.g., `.context/security.md`).

### Debugging Context Resolution
To verify what an AI agent "sees" for a specific path, use the context loader:
```bash
# Verify backend context
python3 scripts/context_loader.py --path app/backend

# Verify frontend context with security overlay
python3 scripts/context_loader.py --path app/frontend --task security
```

### Adding New Contexts
1. Create `.context.md` in the target directory.
2. Define rules, library preferences, or architectural details specific to that scope.
3. The nearest `.context.md` file will always take priority in resolution.