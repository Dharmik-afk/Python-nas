# Track Specification: Copyparty Integration Refactor

## 1. Overview
The goal of this track is to deepen the integration with `copyparty` to serve as the robust backend engine for all file-related operations. This involves replacing custom Python implementation details with proxied requests to the running `copyparty` instance, thereby reducing code maintenance, improving performance (thumbnails, streaming), and ensuring consistency. We will also remove legacy code that is no longer needed.

## 2. Goals
- **Eliminate Redundancy:** Remove custom file serving and thumbnail generation logic in favor of `copyparty`'s built-in features.
- **Improve Performance:** Leverage `copyparty`'s optimized media streaming and thumbnail caching.
- **Legacy Cleanup:** Safely remove the `src/` directory and any unused endpoints in `backend/app`.
- **Standardization:** Ensure all file operations (List, Upload, Download, Preview) flow through a consistent architectural pattern (FastAPI Proxy -> Copyparty).

## 3. Scope
### In Scope
- **Analysis:** Reviewing `backend/app` for duplicate logic.
- **Refactoring:**
    - `backend/app/routes` (API and Views) to proxy specific paths to `copyparty`.
    - Thumbnail generation logic.
    - Media streaming endpoints.
- **Deletion:** Removing `src/` directory.
- **Configuration:** Tuning `copyparty` flags in `run.sh` or `backend/app/core` if necessary to support the integration.

### Out of Scope
- **UI Redesign:** The frontend look and feel should remain largely the same, just powered by different backend logic.
- **Auth System Replacement:** While `copyparty` has auth, we are keeping the FastAPI auth layer as the primary gatekeeper for now, simply passing trusted requests to `copyparty` (or using it as a backend service).

## 4. Technical Details
- **Proxy Mechanism:** We will likely use `httpx` or standard `requests` (streaming) to proxy requests from FastAPI to `localhost:<copyparty_port>`.
- **Endpoints to Refactor:**
    - `/thumbnail/{path}` -> Proxy to `copyparty`'s `.th` endpoints.
    - `/stream/{path}` -> Proxy to `copyparty`'s raw file endpoints (supporting Range headers).
    - `/zip/{path}` -> Proxy to `copyparty`'s download/zip features.

## 5. Success Criteria
- [ ] `src/` directory is removed.
- [ ] No custom `Pillow`/`PIL` image resizing code remains in the FastAPI app (delegated to `copyparty`).
- [ ] Video seeking works flawlessly (Byte-range support verified).
- [ ] Directory listing is accurate and syncs with `copyparty`'s view.
