# Track Specification: Advanced Media Preview System (V3)

## Overview
This track implements a high-fidelity, mobile-optimized media preview system. It combines the aesthetic and organizational logic of Google Photos (minimalist UI, slide-up details) with the interactive power of MX Player (gesture-based video controls). The system is designed for speed, utilizing prefetching and Service Worker caching to minimize loading times.

## Functional Requirements
*   **Unified Media Lightbox:**
    *   Full-screen overlay for photos and video streaming.
    *   **Navigation:** horizontal touch-swipe support for traversing folder contents (restricted to images and videos).
    *   **Document Exclusion:** Documents can be viewed but are isolated; users cannot swipe from a document to media or vice versa.
*   **Performance & Caching:**
    *   **Photo Prefetching:** Automatically load adjacent photos in the background.
    *   **Video Thumbnails:** If the next/prev item is a video, only prefetch its thumbnail, not the full stream.
    *   **Service Worker Caching:** Implement a Service Worker to cache media content (especially video chunks) for instant replay and reduced buffering.
*   **Video Player (MX Player Inspired):**
    *   **Interaction:** Auto-hiding controls with a prominent centered Play/Pause button.
    *   **Gestures (on content):** Vertical swipes for volume/brightness; horizontal swipes for seeking.
*   **UI & Gestures (Google Photos Inspired):**
    *   **Action Bar:** Minimalist top/bottom icons for Download, Details, and permission-based Rename/Delete.
    *   **Exit Gesture:** A vertical swipe on the background overlay or UI (non-media area) closes the preview.
    *   **Details Panel:** Slide-up "Bottom Sheet" displaying filename, size, date, and resolution.
*   **Adaptive UI:**
    *   Management actions (Rename/Delete) dynamically show/hide based on the user's `pmask`.

## Technical Requirements
*   **Frontend:** Alpine.js for UI state and gesture handling. Service Workers for media caching.
*   **Libraries:** Potential use of PhotoSwipe (gallery) or Plyr (video) if they support the required customization.
*   **Backend:** Existing `/api/v1/fs` endpoints for metadata; ensure streaming is compatible with Service Worker range requests.

## Acceptance Criteria
*   Swipe navigation works fluidly between images and videos.
*   Videos start playback quickly and support instant replay via cache.
*   Vertical swipe on background closes the lightbox.
*   "Details" sheet provides accurate media info.
*   Read-only users do not see management icons.

## Out of Scope
*   Music/Audio-only player.
*   Swiping between documents.
*   Server-side video transcoding.
