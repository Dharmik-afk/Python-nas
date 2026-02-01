# DEBUG.md — Project Debug Context
**Version:** 3.4.1
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

### Issue: PyPy 3.11 + Cryptography on Termux
- **Status:** **WORKAROUND ACTIVE**
- **Symptom:** `ImportError: No module named 'cryptography'` when running with `USE_PYPY=true`.
- **Root Cause:** `cryptography` requires Rust to build from source on PyPy. The system-wide `python-cryptography` package in Termux is built for CPython 3.12 and is binary-incompatible with PyPy.
- **Workaround:** `app/core/auth.py` now uses a conditional import for `cryptography`. If missing, it falls back to plain-text for session auth headers.
- **Security Impact:** Session auth headers (internal proxy credentials) are stored in plain-text in the session database when running under PyPy without the `cryptography` library.

### Issue: logger Import Failure in app/core/auth.py
- **Status:** **FIXED**
- **Symptom:** `ImportError: cannot import name 'logger' from 'app.core.logger'`
- **Root Cause:** Incorrect import statement `from .logger import logger` in a file that doesn't export a `logger` variable.
- **Fix:** Replaced with standard `logging.getLogger(__name__)`.

### Issue: uv + PyPy Libc Detection
- **Status:** **WORKAROUND ACTIVE**
- **Symptom:** `uv venv` or `uv sync` fails with `Could not detect a glibc or a musl libc` when targeting PyPy.
- **Workaround:** Use `pypy3 -m venv` for environment creation and `pip install -r requirements-pypy.txt` (exported via `uv export`) for dependency management in the PyPy environment.

### Issue: Health Check Shadowing
- **Status:** **FIXED**
- **Fix:** Moved `/health` endpoint definition above router inclusions in `app/main.py`.

---

## 2. Project Execution Model

### Language & Runtime Stack
- Python 3.12 (FastAPI / CPython)
- PyPy 3.11 (Experimental support via `USE_PYPY=true`)
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

---

## 5. Context Hierarchy (Scoped AI Instructions)

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

