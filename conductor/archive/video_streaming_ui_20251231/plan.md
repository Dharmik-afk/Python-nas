# Plan: Improved Video Streaming UI & Mobile Experience

This plan follows the Test-Driven Development (TDD) workflow and the Phase Completion Verification and Checkpointing Protocol defined in `conductor/workflow.md`.

## Phase 1: Custom Minimalist UI Foundation [checkpoint: 603e8b4]
Goal: Replace native browser controls with a custom-styled, functional control bar.

- [x] Task: Scaffolding - Create the base HTML structure and CSS for the custom video player. ded3976
    - [ ] Create `app/frontend/templates/partials/video_player.html`.
    - [ ] Create `app/frontend/static/css/video_player.css`.
- [x] Task: Basic Controls Logic (TDD) - Implement Play/Pause and Seek functionality. 3013e5d
    - [x] Red Phase: Write failing tests for play/pause and seek state in a new test file `app/tests/test_video_player_controls.py`.
    - [x] Green Phase: Implement logic in Alpine.js or vanilla JS within the partial.
    - [x] Refactor: Clean up JS event listeners and CSS transitions.
- [x] Task: Time & Volume Display (TDD) - Implement current time, duration, and volume slider. 3013e5d
    - [x] Red Phase: Write failing tests for time formatting and volume updates.
    - [x] Green Phase: Implement time tracking and volume control logic.
- [x] Task: Fullscreen Toggle (TDD) - Implement a custom fullscreen button. 3013e5d
    - [x] Red Phase: Write failing tests for entering/exiting fullscreen mode.
    - [x] Green Phase: Implement `requestFullscreen` and `exitFullscreen` wrapper.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Custom Minimalist UI Foundation' (Protocol in workflow.md)

## Phase 2: Intelligent Mobile Orientation & Scaling
Goal: Implement orientation locking/triggering and aspect-ratio-aware scaling for mobile devices.

- [x] Task: Aspect Ratio Detection (TDD) - Implement logic to detect video dimensions and categorize aspect ratio. ac37efd
    - [x] Red Phase: Write tests that verify detection of 16:9, 4:3, and 2.39:1 videos.
    - [x] Green Phase: Implement `loadedmetadata` event handler to calculate ratio.
- [x] Task: Orientation Trigger Logic (TDD) - Automatically suggest/trigger landscape for horizontal videos on mobile. ac37efd
    - [x] Red Phase: Mock Screen Orientation API and verify orientation change calls for horizontal videos.
    - [x] Green Phase: Implement orientation lock/request logic using Screen Orientation API.
- [x] Task: Manual Rotation Button (TDD) - Add a UI button to manually rotate the view. ac37efd
    - [x] Red Phase: Write tests for the manual override button state and orientation toggle.
    - [x] Green Phase: Implement the manual rotation button and associated CSS transforms/orientation calls.
- [x] Task: Responsive Scaling (CSS) - Ensure the video container scales correctly for all horizontal formats. ac37efd
    - [x] Implement CSS for letterboxing/pillarboxing using object-fit and flexbox.
    - [x] Verify 4:3 and ultra-wide (2.39:1) rendering on mobile viewports.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Intelligent Mobile Orientation & Scaling' (Protocol in workflow.md) - Superseded by video_framework_20260101

## Phase 3: Visual Polish & UX Refinement
Goal: Add finishing touches like auto-hiding controls and buffering indicators.

- [x] Task: Buffering & Loading Indicator (TDD) - Show a spinner when the video is stalled or loading. - Superseded by video_framework_20260101
    - [x] Red Phase: Write tests that check for the presence of a spinner when the `waiting` event fires. - Superseded by video_framework_20260101
    - [x] Green Phase: Implement the visual spinner and event listeners (`waiting`, `playing`, `canplay`). - Superseded by video_framework_20260101
- [x] Task: Auto-hide Controls (TDD) - Implement logic to hide the control bar after inactivity. - Superseded by video_framework_20260101
    - [x] Red Phase: Write tests to verify the control bar's "hidden" class is applied after a timeout. - Superseded by video_framework_20260101
    - [x] Green Phase: Implement `setTimeout` and mouse/touch movement listeners to toggle control visibility. - Superseded by video_framework_20260101
- [x] Task: Integration & Cleanup - Final visual audit and CSS minification/optimization. - Superseded by video_framework_20260101
    - [x] Audit all transitions and ensure 80%+ code coverage for new JS/Python code. - Superseded by video_framework_20260101
- [x] Task: Conductor - User Manual Verification 'Phase 3: Visual Polish & UX Refinement' (Protocol in workflow.md) - Superseded by video_framework_20260101
