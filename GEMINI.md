# Gemini CLI Agent — Project Context
Version: 2.3.0 (Architecture 2.0 + Media Preview V3)

## Agent Identity
- Name: gemini-cli-agent
- Role: Codebase Operational Auditor & Developer
- Focus: Architecture 2.0 (Single-Port, Supervisor-Driven)
...
### 4. Integration State
- **FastAPI Handshake**: Every login performs a real-time verification handshake with Copyparty.
- **Single-Source-of-Truth**: All user data resides in SQLite (`storage/db/server.db`).

### 5. Advanced Media Preview (V3)
- **High-Performance Lightbox**: Mobile-optimized gallery using Alpine.js for state management and complex gesture handling.
- **Service Worker (`sw.js`)**: Intercepts media requests and handles Range Requests for "zero-loading" video streaming and persistent caching.
- **MX Player Inspired Controls**: Vertical swipes for volume/brightness, double-tap skip, and intelligent auto-hiding playback controls.
- **Google Photos Aesthetic**: Minimalist split layout with a floating details popover and permission-aware management actions (Rename/Delete).

## Execution Protocol
1.  **Configure**: Edit `.env` or run `make set-dir dir=/path/to/media`.
2.  **Run**: `make run` (triggers `scripts/run.sh`).
3.  **Logs**: Centralized in `logs/server.log`.

## Active Extensions
- project-inspector (Manages DEBUG.md)
- python-dev (Standard Python rules)
- workflow-safety (Shell execution policies)