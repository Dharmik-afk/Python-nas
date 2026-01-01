# Specification: Integrate Artplayer.js for Robust Video Streaming

## 1. Overview
This track aims to replace the current custom-built video player implementation with **Artplayer.js**. The goal is to leverage a robust, maintained framework that provides better cross-browser compatibility and built-in features while retaining high customizability. A key requirement is to replicate and refine mobile-friendly gestures, specifically double-tap seeking.

## 2. Functional Requirements

### 2.1 Core Integration
-   [ ] **Library Replacement:** Remove the existing custom `video_player.js` logic and replace it with Artplayer.js.
-   [ ] **Stream Binding:** Ensure Artplayer correctly consumes the existing backend video stream (served via HTTP Range requests).
-   [ ] **Asset Management:** Add Artplayer.js (and its dependencies/CSS) to the project's static assets.

### 2.2 User Interface & Controls
-   [ ] **Double-Tap to Seek:** Implement custom logic or configure Artplayer to support:
    -   Double-tap on the **left side** to rewind 10 seconds.
    -   Double-tap on the **right side** to fast-forward 10 seconds.
    -   (Optional) Display visual feedback (e.g., ripple or "-10s" text) on tap.
-   [ ] **Standard Controls:** Ensure the following default controls are available and styled to match the application's "Google Photos" aesthetic (minimalist):
    -   Play/Pause
    -   Timeline/Progress Bar
    -   Volume/Mute
    -   Fullscreen toggle
    -   Playback Speed selection (0.5x - 2.0x)

### 2.3 Mobile Optimization
-   [ ] **Responsive Container:** The player must resize correctly within the existing Lightbox/Modal view on both mobile and desktop.
-   [ ] **Auto-Orientation:** (If currently supported) Respect existing logic for auto-rotating landscape videos on mobile.

## 3. Non-Functional Requirements
-   **Visual Consistency:** The player theme should blend with the current dark/neutral palette.
-   **Performance:** The library should only be initialized when the video modal is opened to avoid slowing down the file browsing grid.

## 4. Out of Scope
-   Adaptive Bitrate Streaming (HLS/DASH) implementation (backend remains unchanged).
-   Playlist support.