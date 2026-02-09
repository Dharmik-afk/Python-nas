# Implementation Plan: Dynamic Site Opener (Supervisor-led)

## Phase 1: Preparation & Logic Design
- [x] Task: Research dynamic URL sources. Identify where the "dynamic ID" or URL originates (e.g., `.env`, local IP, or a tunnel service). [no-code-change]
- [x] Task: Design the script generation logic in a new utility file or within Supervisor. [no-code-change]

## Phase 2: Implementation
- [x] Task: Implement URL detection. [code-change]
    - [x] Create `app/core/utils.py` function (or update existing) to determine the "Public" URL (Tunnel > LAN IP > Localhost).
- [x] Task: Implement script generation. [code-change]
    - [x] Create a function `generate_opener_script()` that writes `open_server.sh`.
- [x] Task: Integrate with Supervisor. [code-change]
    - [x] Modify `supervisor/supervisor.py` to call `generate_opener_script()` at startup.

## Phase 3: Verification [checkpoint: 778bbb8]
- [x] Task: Start the server and verify `open_server.sh` is created. [verified]
- [x] Task: Verify the content of `open_server.sh` matches the expected `am start` format and current URL. [verified]
- [x] Task: Execute `./open_server.sh` manually to ensure it opens the browser. [verified command]
- [x] Task: Conductor - User Manual Verification 'Phase 3: Verification' (Protocol in workflow.md) [verified]
