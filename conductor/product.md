# Initial Concept
A lightweight, extendable Python-based file server optimized for private network use on Android via Termux. It provides a modern, responsive web interface for managing and streaming media from local storage.

# Product Guide - Python FastAPI File Server

## Executive Summary
A lightweight, extendable Python-based file server optimized for private network use on Android via Termux. It provides a modern, responsive web interface for managing and streaming media from local storage.

## Target Audience
- **Home Lab Enthusiasts:** Individuals hosting media and files on their private home network using Android devices (Termux).

## Core Goals
- **Android Integration:** Seamlessly serve files from Android storage within the Termux environment.
- **Efficient Streaming:** Provide a fast, reliable gallery and media streaming experience.
- **Ease of Use:** Simple setup and maintenance via a web-based frontend.

## Key Features
- **Modern UI:** Responsive, single-page feel using FastAPI, Jinja2, and HTMX.
- **Media Gallery:** Immersive preview and streaming for images, videos, and music.
- **Jail Security:** Strict filesystem confinement to the configured stream directory.
- **Path Obfuscation:** Security-through-obscurity by returning 404 for restricted paths.
- **Environment-Driven:** Fully configurable via `.env` for easy deployment in Termux.
- **Copyparty Backend:** Robust file handling and thumbnail generation.
- **Private Network Security:** Designed for secure access within a LAN.

## Future Roadmap
- **Client-Side Application:** Development of a dedicated client-side application for enhanced user experience and native device integration.
