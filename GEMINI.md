# Gemini Code Analysis: Python File Server (FastAPI)

This document provides a summary of the refactored Python file server, as analyzed and improved by the Gemini CLI.

## Project Overview

The project is a lightweight, extendable Python-based file server, refactored to use the FastAPI framework and Jinja2 templating with `htmx` and `Alpine.js`. It leverages `copyparty` as a high-performance backend engine for file operations, thumbnail generation, and media streaming.

## System Architecture & Logic

### 1. Dual-Server Proxy Model
The application operates as a **Reverse Proxy + Enhanced Frontend**.
- **FastAPI (Frontend)**: Acts as the primary entry point, handling the modern UI, request validation, security filtering, and session management.
- **Copyparty (Backend Engine)**: A managed subprocess that handles heavy-duty file system tasks, byte-range streaming (for video seeking), and thumbnail processing.

### 2. Core Components
- **Lifecycle Management (`main.py` & `copyparty_manager.py`)**: Orchestrates the startup and shutdown of both servers. Uses standard signal handling and `start_new_session=True` for reliable subprocess management.
- **Selective Async Proxying (`copyparty_proxy.py`)**: Selectively forwards requests to the backend using `httpx`. It preserves **Range headers** for video playback and proxies file uploads via `PUT` requests without blocking the event loop.
- **Security Guard (`file_security.py`)**: Every request is validated using `validate_and_resolve_path`, which uses absolute resolution to prevent directory traversal attacks.
- **Dynamic Frontend**: 
    - **HTMX**: Enables navigation without full page reloads by swapping only the file list component.
    - **Alpine.js**: Powers the interactive media lightbox and UI state management.
- **Async Metrics Tracking (`metrics.py`)**: Uses `aiofiles` and `asyncio.Lock` to persist server statistics (uploads, downloads, errors) without blocking the event loop.

## Recent Improvements

### Code Deduplication & Optimization
*   **Centralized Constants**: Consolidated forbidden files and previewable extension lists into `backend/app/core/constants.py`.
*   **Shared Templates**: Centralized `Jinja2Templates` initialization in `backend/app/core/templates.py` and exposed `PREVIEWABLE_EXTENSIONS` globally to templates.
*   **Path Management**: Added a `SERVE_PATH` property to the Pydantic `Settings` class for consistent and efficient `Path` object handling.
*   **Async Refactor**: Replaced `requests` with `httpx` throughout the application (proxying, auth, API calls), ensuring the FastAPI event loop is never blocked by network I/O.
*   **Performance**: Refactored metrics tracking to be fully asynchronous, preventing I/O bottlenecks during concurrent requests.
*   **Cleanup**: Removed over-engineered keyboard listeners and redundant login proxy logic.

### Maintenance & Resilience
*   **Integrated Logging**: Redirected `copyparty` subprocess output to the main application logger, prefixed with `[Copyparty]`, for unified debugging.
*   **Venv Optimization (Termux)**: Re-configured the virtual environment with `--system-site-packages` to leverage native modules (`cryptography`, `bcrypt`) installed via `pkg` on Android.
*   **Proxy Hardening**: Improved `proxy_upload_request` with granular error handling and filename validation.

### Security & Auth
*   **Session-Based Proxying**: Authentication is proxied to Copyparty to obtain and manage session cookies (`cppps`, `cppwd`), ensuring the frontend and backend share the same security context.
*   **Forbidden Filtering**: Automatically hides sensitive files and directories (e.g., `.git`, `.env`, `__pycache__`).

## Core Functionality

*   **Modern Backend:** FastAPI for high performance and asynchronous request handling.
*   **Immersive Media Preview:** Glassmorphism lightbox for images, videos, and code.
*   **Mobile-First Design:** Responsive UI with optimized touch targets and swipe gestures.
*   **Efficient Operations:** Instant video seeking (Range support) and fast directory zipping via Copyparty.

## How it Works

1.  **Startup**: `run.sh` initializes the environment and launches FastAPI. `CopyPartyManager` then spawns the backend engine and manages its configuration.
2.  **Authentication**: Users log in via the FastAPI UI. The request is proxied to the backend, which returns session cookies that are forwarded to the client's browser.
3.  **Browsing**: When a user enters a folder, HTMX requests a partial HTML update. FastAPI resolves the path, checks permissions (`pmask`), and filters the contents before rendering.
4.  **Media Streaming**: Media requests are proxied with stream support. The backend engine provides the raw bytes, allowing the browser to handle partial content (buffering/seeking) natively.
5.  **Gallery Preview**: Alpine.js fetches metadata for all previewable items in a directory via the Gallery API, enabling a seamless slideshow experience.