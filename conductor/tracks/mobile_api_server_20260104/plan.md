# Implementation Plan: Mobile API Support (Server-Side)

## Phase 1: Groundwork & Security [checkpoint: 5a36bb5]
- [x] **Task 1: Configure CORS for Mobile Development** (67230fe)
  - Update `app/main.py` to include `CORSMiddleware`.
  - Allow origins typical for mobile development (e.g., `http://localhost`, `http://10.0.2.2` for Android emulator).
  - Use environment variables to make origins configurable.
- [x] **Task 2: Verify and Refine Bearer Token Authentication** (67230fe)
  - Ensure `app/core/auth.py` and route dependencies correctly extract tokens from the `Authorization: Bearer <token>` header.
  - Test the `/api/v1/auth/token` endpoint to ensure it returns a valid JWT with appropriate expiration.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Groundwork & Security' (Protocol in workflow.md) (5a36bb5)

## Phase 2: JSON File System API
- [ ] **Task 3: Implement JSON Directory Listing Endpoint**
  - Create/Update an endpoint `GET /api/v1/fs/list/{path:path}`.
  - Define a Pydantic schema for file/folder objects (name, size, type, permissions, mtime).
  - Implement TDD: Write failing tests in `app/tests/test_mobile_api.py` first.
- [ ] **Task 4: Implement JSON Search Results Endpoint**
  - Modify `GET /api/v1/fs/search` to detect an `Accept: application/json` header or a `format=json` query parameter.
  - Ensure the search logic returns the same underlying data structure as the directory listing.
  - Implement TDD: Write failing tests for JSON search response.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: JSON File System API' (Protocol in workflow.md)

## Phase 3: Media Metadata API
- [ ] **Task 5: Refine Gallery JSON Endpoint**
  - Verify `GET /api/v1/gallery/{path:path}` returns a clean, mobile-ready JSON array.
  - Ensure all necessary streaming and thumbnail URLs are absolute or correctly relative to the server root.
  - Implement TDD: Verify gallery metadata structure via tests.
- [ ] **Task 6: Verify Thumbnail Proxy for Mobile Access**
  - Ensure the `?thumb=WxH` parameter on download routes is correctly handled for mobile clients.
  - Verify that authentication is enforced for thumbnail generation when using Bearer tokens.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Media Metadata API' (Protocol in workflow.md)

## Phase 4: Finalization & Quality Assurance
- [ ] **Task 7: API Documentation & Schema Review**
  - Review the auto-generated Swagger UI (`/docs`) to ensure all mobile API schemas are correctly documented and named.
- [ ] **Task 8: Comprehensive Mobile API Test Suite**
  - Run a full test pass covering all mobile endpoints with valid, expired, and missing tokens.
  - Ensure coverage meets the >80% requirement for the new API modules.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Finalization & QA' (Protocol in workflow.md)
