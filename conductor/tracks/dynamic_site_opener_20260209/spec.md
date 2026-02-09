# Specification: Dynamic Site Opener Script

## Overview
Create a mechanism that automatically generates a shell script (`open_server.sh`) whenever the NAS server starts. This script will contain the current dynamic URL (Host/Port/Tunnel ID) and a command to open it in the Android default browser using Termux's ability to call Android intents.

## Functional Requirements
1. **Auto-Generation**: A script named `open_server.sh` must be created or updated in the project root every time the Supervisor starts the server.
2. **Dynamic URL Detection**: The generator must resolve the correct host and port (or tunnel URL) from the application settings or environment.
3. **Browser Integration**: The generated script must use the Android Intent system to open the URL:
   `am start -a android.intent.action.VIEW -d <URL>`
4. **Supervisor Integration**: `supervisor/supervisor.py` must be responsible for triggering this generation at startup.
5. **Non-Blocking**: The generation of the script must not delay the server startup.

## Non-Functional Requirements
- **Simplicity**: The generated script should be a simple, one-line executable `bash` script.
- **Permission**: The generator must ensure the script has execute permissions (`chmod +x`).

## Acceptance Criteria
- Starting the server (via `make run`) creates/updates `open_server.sh`.
- Running `./open_server.sh` from another Termux session opens the correct NAS UI in the browser.
- The script contains the correct dynamic URL even if the port or host is changed in `.env`.

## Out of Scope
- Automatic browser login (due to browser cookie isolation).
- Support for non-Android operating systems.
