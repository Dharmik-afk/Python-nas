# Specification: Mobile API Support (Server-Side)

## 1. Overview
This track focuses on enhancing the existing FastAPI backend to provide robust, JSON-based API endpoints specifically designed for the companion mobile application. It ensures that authentication, file browsing, and media discovery are accessible via standard RESTful patterns, moving beyond the HTMX-focused partials used by the web interface.

## 2. Functional Requirements
### 2.1 JSON File System API
- **Directory Listing:** Update or create an endpoint (e.g., `GET /api/v1/fs/list/{path}`) that returns a structured JSON array of file/folder objects including:
    - `name`, `path`, `is_dir`, `size`, `mtime`, and `permissions` (r, w, d).
- **Search JSON:** Ensure the search endpoint (`/api/v1/fs/search`) supports a `format=json` query parameter or has a dedicated JSON sibling to return results as data rather than HTML.

### 2.2 Authentication & Security
- **Bearer Token Support:** Ensure all protected routes accept a `Bearer <JWT>` token in the `Authorization` header.
- **Token Exchange:** Verify the `/api/v1/auth/token` endpoint correctly issues long-lived (or refreshable) tokens suitable for mobile app sessions.
- **CORS Policy:** Implement a configurable CORS policy in `app/main.py` to allow requests from the React Native development environment (e.g., `localhost` or specific local IPs).

### 2.3 Media Metadata API
- **Gallery JSON:** Ensure the `GET /api/v1/gallery/{path}` endpoint is fully optimized for JSON consumption, providing all necessary URLs for thumbnails and original files.
- **Thumbnail Stability:** Ensure thumbnail generation via `?thumb=WxH` is consistent and works reliably when accessed via the mobile client's token.

## 3. Technical Requirements
- **Response Schemas:** Define Pydantic models for all new JSON responses to ensure type safety and consistent API documentation (Swagger/ReDoc).
- **Test Suite:** Create a new test file `app/tests/test_mobile_api.py` to verify all JSON endpoints with Bearer token authentication.

## 4. Acceptance Criteria
- [ ] New/Updated JSON endpoints return valid JSON according to defined Pydantic schemas.
- [ ] Authentication works via the `Authorization: Bearer <token>` header for all mobile-relevant endpoints.
- [ ] Automated tests pass for directory listing, search, and gallery metadata in JSON format.
- [ ] CORS is configured to allow mobile development connections.

## 5. Out of Scope
- Implementation of the React Native application (handled in the `Client-Side` track).
- Changes to the HTMX-based web frontend.
