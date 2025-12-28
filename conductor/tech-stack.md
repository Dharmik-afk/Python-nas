# Technology Stack - Python FastAPI File Server

## Backend
- **Language:** Python 3.10+
- **Web Framework:** FastAPI (High performance, modern ASGI framework)
- **ASGI Server:** Uvicorn
- **File Engine:** `copyparty` (Primary backend for all file operations, thumbnails, streaming, and upload handling to maximize efficiency)
- **Authentication:** Basic Auth / OAuth2 (using `passlib` with `bcrypt`)

## Database & Persistence
- **ORM:** SQLAlchemy (with SQLite backend)
- **Migrations:** Alembic
- **Configuration:** Pydantic (Settings management)

## Frontend
- **Templating:** Jinja2 (Server-side rendering)
- **Dynamic Interactivity:** HTMX (Low-complexity, high-interactivity AJAX)
- **Client-side Logic:** Alpine.js (Lightweight reactive framework)
- **Styling:** Bootstrap 5 (Responsive grid and utility classes)
- **Icons:** Bootstrap Icons

## Development & Infrastructure
- **Testing:** Pytest, HTTPX (API testing)
- **Environment:** Android (Termux)
- **Build System:** Makefile / Bash scripts (`run.sh`)
