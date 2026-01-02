# Product Guide: Python FastAPI File Server

## Initial Concept
A lightweight, extendable Python-based file server designed for private network use, serving as a unified frontend for the `copyparty` engine.

## Target Audience
The primary audience for this server consists of **home users** who require a reliable and straightforward solution for private network file storage and media management.

## Core Goals
*   **Intuitive Web Interface:** Provide a simple and easy-to-use web interface for browsing, searching, and downloading files.
*   **Secure Private Storage:** Offer a secure method for managing files on a local network, eliminating the need for complex or untrusted cloud-based storage.

## Future Goals
*   **Dedicated Client Applications:** Develop native client-side applications for mobile and desktop platforms to offer offline access, background file synchronization, and a more integrated OS experience.

## Key Features

*   **Mobile-First Design:** A fully responsive user interface ensuring a seamless experience across mobile phones, tablets, and desktop computers.

*   **Unified Frontend:** Acts as a modern wrapper and management layer for the robust `copyparty` file-serving engine.

*   **Granular Access Control:** Transparently enforces `copyparty` permissions (Read, Write, Delete) through a dynamic UI that adapts to the user's authorization level.

*   **Integrated File Management:** Supports core file operations including browsing, downloading, multi-file uploading, and folder creation.

*   **Advanced Media Playback:** Features a robust, gesture-controlled video player (Artplayer.js) with mobile-optimized controls (double-tap seek, swipe for volume/brightness), intelligent orientation locking (auto-landscape for horizontal videos), and playback speed adjustment. Videos present a clean thumbnail preview before playing to maintain visual consistency.



## User Experience (UX) Design

The application aims for a dual-layered experience:

*   **Standard Users:** A **fast, lightweight, and modern** interface. It uses a clean design to minimize loading times and prioritize ease of navigation.

*   **Context-Aware Interface:** The UI dynamically hides or shows management features (like Upload, Create Folder, or Delete) based on the current user's verified permissions, ensuring a clean and secure experience.
