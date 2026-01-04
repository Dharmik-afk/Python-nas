# Plan: React Native Client App (Expo + Zustand) on Termux

This plan is optimized for the Termux environment on Android, utilizing Expo (Managed Workflow) and Zustand for state management. It strictly avoids native tooling dependencies.

## Phase 1: Project Scaffolding & Setup (Termux/Expo) [checkpoint: d68005d]
- [x] **Task 1: Environment Verification** 94f5efb
  - Verify `node -v` and `npm -v`.
  - Install Node.js via Termux pkg if missing (`pkg install nodejs`).
  - Verify global Expo CLI is NOT needed (we will use `npx`).
- [x] **Task 2: Initialize Expo Project** ae914cd
  - Run `npx create-expo-app ClientApp`.
  - **Constraint:** Do NOT use React Native CLI.
  - Create the enforced directory structure: `store/`, `components/`, `screens/`.
- [x] **Task 3: Install Core Dependencies** afe74f7
  - Install State Manager: `npm install zustand`
  - Install Navigation: `npm install @react-navigation/native react-native-screens react-native-safe-area-context @react-navigation/stack`
  - Install List Component: `npx expo install @shopify/flash-list`
  - Install Storage (for persistence): `npx expo install @react-native-async-storage/async-storage`
  - Install Media/Gestures: `npx expo install expo-av react-native-gesture-handler`
- [x] **Task 4: Create Mobile Context (GEMINI.md)** 65f15d6
  - Create `ClientApp/GEMINI.md` containing the "React Native App (Expo + Zustand) on Termux" context rules to guide future sub-agents.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Project Scaffolding' (Protocol in workflow.md)

## Phase 2: Authentication & Security [checkpoint: 6a98adc]
- [x] **Task 5: Implement Auth Store (Zustand)** 104c0e8
  - Create `store/useAuthStore.js`.
  - Implement actions: `login`, `logout`, `setServerUrl`.
  - Implement persistence using `persist` middleware (storing `serverUrl` and `accessToken`).
- [x] **Task 6: Implement Login Screen** 51037c4
  - Create `screens/LoginScreen.js`.
  - UI: Minimalist "Google Photos" style entry for Server URL and Password.
  - Integration: Connect to server's `/api/v1/auth/token` via `fetch`.
  - Error Handling: Display clear error messages (e.g., "Connection Failed", "Invalid Credentials").
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Authentication' (Protocol in workflow.md)

## Phase 3: File Explorer (Google Photos Aesthetic)
- [ ] **Task 7: Implement Data Store (Zustand)**
  - Create `store/useFileStore.js` to manage directory contents and caching.
- [ ] **Task 8: Implement Directory Grid View**
  - Create `screens/ExplorerScreen.js`.
  - Use `FlashList` to render a high-performance grid of media items.
  - **Constraint:** Ensure `numColumns` adapts to screen width.
- [ ] **Task 9: Navigation Logic**
  - Update `App.js` to implement a Stack Navigator.
  - Handle navigation between `LoginScreen` and `ExplorerScreen`.
  - Implement drill-down navigation for folders.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: File Explorer' (Protocol in workflow.md)

## Phase 4: Media Player (Expo AV)
- [ ] **Task 10: Integrate Video Player**
  - Create `screens/PlayerScreen.js`.
  - Use `expo-av` (`Video` component) for playback.
  - **Constraint:** Do NOT use `react-native-video` (avoids native linking issues in Termux).
- [ ] **Task 11: Implement Gestures**
  - Use `react-native-gesture-handler` to implement:
    - Double-tap to seek.
    - (Optional) Vertical swipe for brightness/volume (if feasible with Expo libraries, otherwise provide on-screen sliders).
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Media Player' (Protocol in workflow.md)