# Product Guidelines - Python FastAPI File Server

## Visual Identity
- **Theme:** Modern Dark Mode with high-contrast elements.
- **Design Language:** Glassmorphism (translucent, blurred backgrounds) to create depth and hierarchy.
- **Color Palette:**
  - **Primary:** Gradient (Bootstrap Primary to Purple `#6f42c1`)
  - **Background:** Dark body background with animated "blobs" for visual interest.
  - **Accents:** White text with varying opacity for hierarchy (100%, 70%, 50%).
- **Typography:** Clean, sans-serif fonts. Headings use heavy weights (Bold/Black) for impact.
- **Iconography:** Bootstrap Icons (`bi-`) used extensively for visual cues.

## User Experience (UX)
- **Navigation:** Sticky top navbar with glass effect. Breadcrumbs for directory traversal.
- **Interactivity:**
  - **HTMX:** Used for server-driven UI updates (navigation, file listings) without full page reloads.
  - **Alpine.js:** Handles client-side state (Lightbox, Login form validation, Dropdowns).
- **Feedback:** Loading spinners, hover effects (transform, shadow), and toast notifications for actions like copying links.
- **Responsiveness:** Mobile-first design using Bootstrap's grid system. Touch gestures (swipe) supported in the lightbox.

## Component Library
- **Cards:** Glass-effect cards for files/folders with hover lift and shadow animations.
- **Lightbox:** Full-screen modal for media preview (Image, Video, Text) with keyboard and touch navigation.
- **Forms:** Modern input fields with animated focus borders and custom checkboxes.
- **Buttons:** Gradient pills with shadow effects and transform animations on hover.

## Code Style (Frontend)
- **HTML:** Semantic structure, accessible attributes (ARIA where needed).
- **CSS:** Scoped styles within templates (for now) or bundled via `bundle.css`. Utility-first classes (Bootstrap) preferred over custom CSS where possible.
- **JS:** Minimal inline JavaScript; prefer declarative directives (HTMX, Alpine) over imperative logic.
