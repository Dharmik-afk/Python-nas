# Implementation Plan: Advanced Media Preview System

This plan details the steps to implement a high-performance, mobile-optimized media preview system inspired by Google Photos and MX Player.

## Phase 1: Performance Infrastructure (Service Worker & Prefetching) [checkpoint: 2c96caf]
Goal: Establish the caching and prefetching foundation for a "zero-loading" experience.

- [x] **Task 1: Service Worker Implementation** (4e3c039)
    - [ ] Sub-task: Create `app/frontend/static/js/sw.js` to intercept media requests.
    - [ ] Sub-task: Implement Range Request caching logic for video streaming chunks.
    - [ ] Sub-task: Register Service Worker in `base.html`.
- [x] **Task 2: Prefetching Engine** (53e52b1)
    - [ ] Sub-task: Implement Alpine.js logic to identify "next" and "previous" media items.
    - [ ] Sub-task: Create logic to fetch full images for adjacent photos.
    - [ ] Sub-task: Create logic to fetch only thumbnails for adjacent videos.
- [ ] **Task: Conductor - User Manual Verification 'Phase 1: Performance Infrastructure' (Protocol in workflow.md)**

## Phase 2: Unified Lightbox & Gesture Navigation [checkpoint: 6345bf1]
Goal: Build the core gallery UI and implement navigation gestures.

- [x] **Task 1: Google Photos Inspired UI** (965de57)
- [x] **Task 2: Content-Aware Gestures** (1b61a6e)
    - [ ] Sub-task: Implement horizontal swipe navigation restricted to image/video content.
    - [ ] Sub-task: Implement vertical "swipe-to-exit" on the background overlay.
    - [ ] Sub-task: Implement logic to isolate document viewing (no swiping into/out of docs).
- [ ] **Task: Conductor - User Manual Verification 'Phase 2: Unified Lightbox & Gesture Navigation' (Protocol in workflow.md)**

## Phase 3: MX Player Inspired Video Player
Goal: Implement the advanced video streaming experience with content-focused gestures.

- [ ] **Task 1: Custom Video Player Integration**
    - [ ] Sub-task: Integrate a lightweight player (e.g., Plyr) or extend native `<video>` with custom controls.
    - [ ] Sub-task: Style the UI with auto-hiding controls and centered Play/Pause.
- [ ] **Task 2: Video Gestures**
    - [ ] Sub-task: Implement vertical swipe on the left side for brightness (CSS overlay).
    - [ ] Sub-task: Implement vertical swipe on the right side for volume.
    - [ ] Sub-task: Implement horizontal swipe for seeking.
- [ ] **Task: Conductor - User Manual Verification 'Phase 3: MX Player Inspired Video Player' (Protocol in workflow.md)**

## Phase 4: Metadata & Adaptive Actions
Goal: Connect the UI to media metadata and enforce permission-based controls.

- [ ] **Task 1: Client-side Metadata Extraction**
    - [ ] Sub-task: Implement Alpine.js/JS logic to probe `naturalWidth`/`videoHeight` once media loads.
    - [ ] Sub-task: Create a formatting utility for file sizes and dates (already in the UI, but needed for the sheet).
    - [ ] Sub-task: Wire the "Details" button to display this extracted info in the bottom sheet.
- [ ] **Task 2: Permission-Aware Action Bar**
    - [ ] Sub-task: Dynamically show/hide Download, Rename, and Delete based on `pmask`.
    - [ ] Sub-task: Ensure HTMX triggers are correctly wired for Management actions within the lightbox.
- [ ] **Task: Conductor - User Manual Verification 'Phase 4: Metadata & Adaptive Actions' (Protocol in workflow.md)**
