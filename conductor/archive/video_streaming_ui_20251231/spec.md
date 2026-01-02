# Specification: Improved Video Streaming UI & Mobile Experience

## Overview
This track focuses on elevating the video playback experience within the web frontend. The primary goals are to replace native browser controls with a polished, minimalist custom UI and to implement intelligent mobile orientation logic that optimizes the viewing area for all horizontal video formats.

## Functional Requirements
1.  **Custom Minimalist UI:**
    -   Replace native HTML5 video controls with a custom-styled control bar.
    -   Include standard controls: Play/Pause, Seek bar, Time display, Volume, and Fullscreen toggle.
    -   UI should auto-hide during inactivity.
2.  **Intelligent Orientation & Scaling (Mobile Only):**
    -   **Dynamic Landscape Trigger:** Automatically trigger or suggest landscape orientation when entering fullscreen for any video with a horizontal aspect ratio (e.g., 16:9, 2.39:1, 4:3, 21:9).
    -   **Comprehensive Aspect Ratio Support:** Ensure all horizontal formats are scaled correctly to maximize the mobile screen area while maintaining original proportions (proper letterboxing/pillarboxing).
    -   **Manual Override:** Provide a dedicated rotation button within the player UI to manually toggle orientation/fullscreen mode regardless of current sensor state.
3.  **Visual Polish:**
    -   Implement smooth transitions for control visibility.
    -   Add a clear buffering/loading indicator.

## Non-Functional Requirements
-   **Performance:** UI interactions must be fluid and not introduce lag to the video stream.
-   **Responsiveness:** The custom player must adapt seamlessly to different screen sizes and orientations.
-   **Browser Compatibility:** Must work reliably on modern mobile browsers (Chrome on Android, Safari on iOS), specifically utilizing the Screen Orientation API where available.

## Acceptance Criteria
- [ ] Video player uses a custom, minimalist UI instead of native browser controls.
- [ ] On mobile, entering fullscreen or using the manual "Rotate" button correctly transitions to landscape for all horizontal aspect ratios.
- [ ] Horizontal videos (16:9, 2.39:1, 4:3, etc.) are scaled to fill as much of the landscape screen as possible without distortion.
- [ ] Controls auto-hide after a few seconds of user inactivity during playback.

## Out of Scope
- Server-side video transcoding or adaptive bitrate (HLS/DASH).
- Implementing complex gestures like brightness/volume swipes.
- Support for DRM-protected content.
