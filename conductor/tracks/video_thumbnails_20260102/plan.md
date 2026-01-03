# Plan: Integrate Video Thumbnail Generation via Copyparty

This plan follows the Test-Driven Development (TDD) workflow and the Phase Completion Verification and Checkpointing Protocol defined in `conductor/workflow.md`.

## Phase 1: Backend Proxy & Configuration [checkpoint: b0ac74f]
Goal: Enable the backend to serve video thumbnails by forwarding requests to Copyparty.

- [x] Task: Backend Proxy Logic (TDD) - Update the download/media route to forward query parameters. b0ac74f
    - [x] Red Phase: Write a test in `app/tests/test_api.py` that requests a video with a `?thumb=400` parameter and expects a successful image response (or a specific header indicating a proxy to copyparty).
    - [x] Green Phase: Modify the proxy logic in `app/backend/routes/download_routes.py` (or equivalent) to pass through all query parameters to the internal `copyparty_service`.
- [x] Task: Verify Copyparty Thumbnail Support - Ensure Copyparty is configured to generate thumbnails. b0ac74f
    - [x] Audit `copyparty/copyparty.conf` to ensure thumbnailing features are enabled and not blocked.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Backend Proxy & Configuration' (Protocol in workflow.md) b0ac74f

## Phase 2: Frontend Integration & Display [checkpoint: ce09e31]
Goal: Update the UI to display the generated thumbnails and implement prefetching.

- [x] Task: Lightbox UI Update (TDD) - Update the video thumbnail mode to use the generated thumbnail. ce09e31
    - [x] Red Phase: Write/update a test in `app/tests/test_artplayer_integration.py` to verify the `<img>` tag in the video thumbnail mode has a `?thumb=` parameter in its `src`.
    - [x] Green Phase: Update `app/frontend/templates/partials/lightbox.html` to use `currentItem.url + '?thumb=800'` (or similar) for the video preview image.
- [x] Task: Refine Prefetch Logic (TDD) - Ensure thumbnails are proactively requested for videos. ce09e31
    - [x] Red Phase: Mock the `fetch` call and verify that `prefetchAdjacent` requests thumbnail URLs for video items.
    - [x] Green Phase: Update the `prefetchAdjacent()` function in `lightbox.html` to handle video items by requesting their thumbnail URL.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Frontend Integration & Display' (Protocol in workflow.md) ce09e31

## Phase 3: Final Polish & Audit [checkpoint: ]
Goal: Ensure stability and remove placeholders.

- [ ] Task: Visual Audit - Confirm that thumbnails load correctly and fall back to the icon only on error.
- [ ] Task: Cleanup - Remove any temporary placeholder assets or debug logs related to thumbnails.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Polish & Audit' (Protocol in workflow.md)
