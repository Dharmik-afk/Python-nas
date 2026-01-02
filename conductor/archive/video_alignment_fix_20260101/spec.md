# Specification: Fix Video Player Alignment Transition

## Overview
This track addresses a critical layout bug in the new "Thumbnail vs. Player" mode implementation. Currently, when switching from the static Thumbnail Mode to the active Video Player Mode, the Artplayer instance misaligns, resulting in most of the video being rendered outside the visible viewport. This issue is particularly noticeable on mobile devices.

## Functional Requirements
1.  **Seamless Transition:** Activating the video player (clicking the Play button) must instantly render the player within the visible bounds of the lightbox container.
2.  **Correct Positioning:** The Artplayer container must be strictly confined to the 100% width and height of its parent container, with no overflow.
3.  **Mobile Stability:** The player layout must remain stable and centered during and after the transition, avoiding any "jumping" or off-screen rendering.

## Acceptance Criteria
- [ ] **Visual Verification:** Clicking "Play" on a video thumbnail results in the video player appearing perfectly centered and fully visible.
- [ ] **No Overflow:** No part of the video player controls or content is cut off or rendered outside the screen edges.
- [ ] **Responsiveness:** The fix works correctly on standard mobile viewports.

## Out of Scope
- Changes to the gesture logic itself (unless directly causing the layout issue).
- Redesign of the thumbnail mode aesthetic.
