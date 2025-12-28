# Track Plan: Copyparty Integration Refactor

## Phase 1: Analysis and Legacy Cleanup [checkpoint: 9acc29f]
**Goal:** Remove unused code and confirm `copyparty` connectivity.

- [x] Task: Analysis - Review existing `backend/app` code to identify custom file handling logic that overlaps with `copyparty`.
- [x] Task: Analysis - Verify `copyparty` configuration in `run.sh` and ensure it exposes necessary APIs.
- [x] Task: Cleanup - Delete the legacy `src/` directory and any references to it in `Makefile` or `run.sh`.
- [x] Task: Cleanup - Remove unused imports or dependencies related to the legacy implementation (e.g., if `socketserver` was used directly).
- [x] Task: Conductor - User Manual Verification 'Analysis and Legacy Cleanup' (Protocol in workflow.md)

## Phase 2: Thumbnail and Media Proxy [checkpoint: 5d7d6a2]
**Goal:** Delegate heavy media lifting to `copyparty`.

- [x] Task: Backend - Implement a generic `proxy_request` utility function in `backend/app/core/utils.py` (or similar) to handle streaming responses from `copyparty`.
- [x] Task: Backend - Refactor `/api/v1/gallery/thumbnail/{path}` to proxy the request to `copyparty`'s thumbnail URL (usually `/{path}?th=...`).
- [x] Task: Backend - Remove local `Pillow` image generation code from `backend`.
- [x] Task: Backend - Refactor media streaming endpoints (if distinct from static serving) to ensure `Range` headers are forwarded to `copyparty` and responses are streamed back.
- [x] Task: Test - Verify that images and videos load correctly in the frontend Lightbox.
- [x] Task: Conductor - User Manual Verification 'Thumbnail and Media Proxy' (Protocol in workflow.md)

## Phase 3: File Operations Refactor [checkpoint: c17c6eb]
**Goal:** Ensure uploads and other file ops use the backend engine.

- [x] Task: Backend - Analyze current Upload implementation. If it writes to disk directly, evaluate if it should be proxied to `copyparty` (PUT/POST) or kept as is (since we have local disk access). *Decision: Keep local write for now if efficient, but ensure metadata sync if needed.* (For this track, we will assume direct disk write is fine for local, but verify path consistency).
- [x] Task: Backend - Refactor `/api/v1/files/zip` (if exists) to use `copyparty`'s packing feature if available, or optimize.
- [x] Task: Conductor - User Manual Verification 'File Operations Refactor' (Protocol in workflow.md)

## Phase 4: Final Verification [checkpoint: 3a419f1]
**Goal:** Ensure system stability.

- [x] Task: Test - Run full integration test: Browse, Preview Image, Stream Video, Download File.
- [x] Task: Documentation - Update `tech-stack.md` if any dependencies were removed.
- [x] Task: Conductor - User Manual Verification 'Final Verification' (Protocol in workflow.md)
