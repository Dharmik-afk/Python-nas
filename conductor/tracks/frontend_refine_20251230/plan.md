# Implementation Plan: Frontend UI/UX Refinement

This plan outlines the steps to refactor frontend components and enhance the user experience with mobile optimizations and action feedback.

## Phase 1: Component Refactoring & Standardization
Goal: Modularize core UI elements into reusable Jinja2 partials and standardize action controls.

- [x] **Task 1: Refactor File Browser Cards** [0c005ae]
    - [x] Sub-task: Create a standalone partial `app/frontend/templates/partials/components/file_card.html`.
    - [x] Sub-task: Update `file_browser_content.html` to use the new card component.
    - [x] Sub-task: Write a test in `app/tests/test_templates.py` to ensure the card partial renders correctly with mock data.
- [x] **Task 2: Standardize Action Buttons and Overlays** [6c4a1e0]
    - [x] Sub-task: Extract Action Buttons (Create, Upload) into `app/frontend/templates/partials/components/action_bar.html`.
    - [x] Sub-task: Extract Action Overlays (Rename, Delete) into a reusable partial or macro.
    - [x] Sub-task: Verify visual consistency across different browser views.
- [~] **Task: Conductor - User Manual Verification 'Phase 1: Component Refactoring & Standardization' (Protocol in workflow.md)**

## Phase 2: Action Feedback System (Toasts)
Goal: Implement a notification system to provide immediate feedback for file operations.

- [ ] **Task 1: Notification Container & Logic**
    - [ ] Sub-task: Add a global toast container to `app/frontend/templates/layouts/base.html`.
    - [ ] Sub-task: Implement a lightweight JavaScript or Alpine.js listener for `show-toast` events.
- [ ] **Task 2: Triggering Toasts via HTMX/Backend**
    - [ ] Sub-task: Update backend routes (`api_routes.py`, `upload_routes.py`) to include `HX-Trigger` headers with success/error messages.
    - [ ] Sub-task: Write integration tests to verify that API responses contain the expected HTMX trigger headers.
    - [ ] Sub-task: Verify that notifications appear correctly for mkdir, upload, rename, and delete actions.
- [ ] **Task: Conductor - User Manual Verification 'Phase 2: Action Feedback System (Toasts)' (Protocol in workflow.md)**

## Phase 3: Mobile UX Audit & Optimization
Goal: Ensure the interface is fully optimized for touch interactions and small screens.

- [ ] **Task 1: Touch Target Audit**
    - [ ] Sub-task: Review all interactive elements (buttons, links, icons) to ensure a minimum size of 44x44px.
    - [ ] Sub-task: Adjust CSS padding/margins for mobile view in `style.css`.
- [ ] **Task 2: Responsive Layout Refinement**
    - [ ] Sub-task: Optimize the breadcrumb navigation for narrow screens (ensure horizontal scroll works smoothly).
    - [ ] Sub-task: Adjust grid spacing and card sizing for very small devices.
- [ ] **Task: Conductor - User Manual Verification 'Phase 3: Mobile UX Audit & Optimization' (Protocol in workflow.md)**
