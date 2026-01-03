# Implementation Plan: React Native Client App (Groundwork)

## Phase 1: Project Scaffolding & Setup
- [ ] **Task 1: Initialize React Native Project**
  - Create the `ClientApp/` directory and ensure it's in the root `.gitignore`.
  - Initialize a new React Native TypeScript project inside `ClientApp/`.
  - Initialize a separate Git repository inside `ClientApp/`.
- [ ] **Task 2: Install Core Dependencies**
  - Install `@react-navigation/native`, `zustand`, `@shopify/flash-list`.
  - Install `react-native-video` and `react-native-gesture-handler`.
  - Install `react-native-vector-icons` (configuring Bootstrap Icons if possible).
- [ ] **Task 3: Create Mobile Context (GEMINI.md)**
  - Create `ClientApp/GEMINI.md` to define instructions for the mobile development sub-agent.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Project Scaffolding' (Protocol in workflow.md)

## Phase 2: Authentication & Security
- [ ] **Task 4: Implement Auth Store (Zustand)**
  - Create a store to manage `accessToken`, `serverUrl`, and `user` profile.
  - Implement persistence for the `serverUrl` and `accessToken`.
- [ ] **Task 5: Implement Login Flow**
  - Create a "Google Photos" style minimalist login screen.
  - Integrate with the server's `/api/v1/auth/token` endpoint.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Authentication' (Protocol in workflow.md)

## Phase 3: File Explorer (Google Photos Aesthetic)
- [ ] **Task 6: Implement Directory Grid View**
  - Use `FlashList` to render a high-performance grid of files/folders.
  - Replicate the card-based design of the web frontend.
- [ ] **Task 7: Folder Navigation**
  - Implement stack navigation to drill down into directories.
  - Fetch JSON metadata from the server's new JSON endpoints.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: File Explorer' (Protocol in workflow.md)

## Phase 4: Media Player & Gestures
- [ ] **Task 8: Integrate Video Player**
  - Implement a full-screen video player using `react-native-video`.
- [ ] **Task 9: Implement Artplayer-style Gestures**
  - Add vertical swipe handlers for Volume and Brightness.
  - Add double-tap handler for seek forward/backward.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Media Player' (Protocol in workflow.md)
