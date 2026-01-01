# Plan: Integrate Artplayer.js for Robust Video Streaming

## Phase 1: Preparation & Asset Integration [checkpoint: 8aaf9d9]
- [x] Task: Research Artplayer.js API for custom gestures and integration with Jinja2 templates. (681e8ee)
- [x] Task: Download Artplayer.js and Artplayer.css and integrate them into `app/frontend/static/`. (a2b258b)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Preparation & Asset Integration' (Protocol in workflow.md)

## Phase 2: Core Replacement [checkpoint: b19c86b]
- [x] Task: Create tests for video player initialization and stream binding. (a77cd41)
- [x] Task: Remove custom legacy video player JS/CSS logic. (d011b88)
- [x] Task: Implement Artplayer.js initialization within the media lightbox. (5b6582c)
- [x] Task: Verify Artplayer correctly consumes the `/download/{path}` stream with Range requests. (5b6582c)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Core Replacement' (Protocol in workflow.md)

## Phase 3: Custom Gesture Logic
- [ ] Task: Write tests for double-tap seeking logic (mocking Artplayer events if necessary).
- [ ] Task: Implement 10-second skip on double-tap for left (rewind) and right (forward) sides.
- [ ] Task: Add visual feedback (e.g., center icons or text overlays) during seeking.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Custom Gesture Logic' (Protocol in workflow.md)

## Phase 4: UI Polish & Mobile Optimization
- [ ] Task: Create tests for responsive behavior and playback controls.
- [ ] Task: Customize Artplayer theme and icons to match the project's minimalist aesthetic.
- [ ] Task: Enable and configure the playback speed selector (0.5x to 2.0x).
- [ ] Task: Ensure the player handles mobile orientation changes and container resizing correctly.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: UI Polish & Mobile Optimization' (Protocol in workflow.md)