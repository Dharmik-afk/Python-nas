# Specification: Integrate Video Thumbnail Generation via Copyparty

## Overview
This track focuses on enabling and integrating video thumbnail generation. Currently, videos use a placeholder icon because thumbnail generation is not active. The goal is to treat video thumbnails similarly to how photos will be handled: by requesting a specific thumbnail version from the backend. This will use Copyparty's built-in thumbnailing capabilities and will be integrated into the frontend's prefetch and display logic.

## Functional Requirements
1.  **Backend Implementation:**
    -   **Proxy Parameter Forwarding:** Update the media proxy (FastAPI) to recognize and forward the `thumb` (or equivalent) query parameter to the internal Copyparty service.
    -   **Copyparty Configuration:** Verify that the `copyparty` instance is configured to allow thumbnail generation (may require checking `copyparty.conf`).

2.  **Frontend Implementation:**
    -   **Lightbox Thumbnail Mode:** Update `app/frontend/templates/partials/lightbox.html` to use the thumbnail URL (e.g., `item.url + '?thumb=400'`) as the `src` for the video preview image.
    -   **Prefetch Logic:** Refine the `prefetchAdjacent()` function to consistently request thumbnails for videos, ensuring they are generated/cached by the backend before the user views them.
    -   **Fallback Handling:** Retain the placeholder icon logic as a fallback if the thumbnail fails to load.

3.  **Consistency:**
    -   The workflow for video thumbnails should set the pattern for future photo thumbnail implementation.

## Acceptance Criteria
- [ ] Video thumbnails (actual frames) are successfully served by the backend when requested.
- [ ] The Lightbox "Thumbnail Mode" displays a generated video frame instead of a static icon.
- [ ] The prefetch logic successfully triggers thumbnail generation for adjacent videos in the gallery.

## Out of Scope
- Implementing thumbnail generation for photos (this track focuses on videos).
- Custom frame selection logic (using Copyparty's defaults).
