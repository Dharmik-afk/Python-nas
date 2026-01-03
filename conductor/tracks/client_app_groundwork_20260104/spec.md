# Specification: React Native Client App (Groundwork)

## 1. Overview
This track focuses on the initial development of the companion mobile application. The app is a **React Native (TypeScript)** project residing in the `ClientApp/` directory. It will be maintained as a standalone project with its own Git repository and `GEMINI.md` context. The UI will mirror the "Google Photos" aesthetic of the web frontend, utilizing minimalist layouts, floating popovers, and a dark-mode-first design.

## 2. Functional Requirements
### 2.1 Project Infrastructure
- **Initialization:** Create a new React Native project with TypeScript in the `ClientApp/` directory.
- **Navigation:** Implement **React Navigation** (Stack and Tab navigators).
- **State Management:** Use **Zustand** for lightweight global state (Auth, UI state, Directory cache).
- **Performance:** Use **FlashList** for high-performance rendering of the file grid.

### 2.2 UI & Aesthetic (Web Parity)
- **Google Photos Aesthetic:** Implement a minimalist grid view for media and list view for files.
- **Components:** Replicate the look and feel of the Bootstrap-based web components (cards, floating action buttons, popovers).
- **Icons:** Use **Bootstrap Icons** (via `react-native-vector-icons` or SVG) to maintain visual consistency.

### 2.3 Authentication & Connectivity
- **Login Interface:** A screen to input server URL, username, and password.
- **Secure Storage:** Store JWT tokens securely.
- **API Integration:** Connect to the new JSON endpoints developed in the server-side track.

### 2.4 File Explorer & Media Player
- **Directory Browsing:** Fetch and display directory listings in a grid/list toggle view.
- **Video Playback:** Integrate `react-native-video` with a UI overlay that mirrors the **Artplayer.js** implementation (custom progress bars, gesture-based volume/brightness).

## 3. Groundwork & Environment
- **Directory Management:** Ensure `ClientApp/` is ignored by the parent project's `.gitignore`.
- **Context:** Initialize a local `GEMINI.md` within `ClientApp/` for specialized agent instructions.

## 4. Acceptance Criteria
- [ ] React Native app initializes and runs on an Android device/emulator.
- [ ] UI matches the server frontend's aesthetic (Google Photos style).
- [ ] User can log in and browse remote files in a high-performance grid.
- [ ] Video playback starts with functional gesture controls matching the web experience.

## 5. Out of Scope
- Support for iOS.
- Full CRUD operations.
- Offline file syncing.
