# Track Plan: Architecture 2.0 Refactor

## Phase 1: Structure and Configuration Alignment
**Goal:** Ensure the filesystem matches `future.md` and resolve configuration race conditions.

- [x] Task: Structure - Verify and create `storage/files`, `storage/cache`, `storage/db`, and `logs` directories (Done).
- [x] Task: Config - Refactor `app/core/user_sync.py` to allow standalone execution (e.g., `if __name__ == "__main__":`).
- [x] Task: Startup - Update `scripts/run.sh` to execute the user sync script *before* launching the supervisor. This prevents Copyparty from loading stale/invalid config.
- [x] Task: Config - Manually clean/reset `copyparty/copyparty.conf` to a valid default state to prevent confusion.
- [ ] Task: Conductor - User Manual Verification 'Structure and Config' (Protocol in workflow.md)

## Phase 2: Supervisor Enhancements
**Goal:** Make the supervisor more robust and integrated with the logging strategy.

- [ ] Task: Supervisor - Update `supervisor/supervisor.py` to write logs to `logs/supervisor.log` instead of just stdout.
- [ ] Task: Supervisor - (Optional) Import `app.core.config` settings in supervisor to avoid hardcoded paths, OR ensure paths are passed as arguments.
- [ ] Task: Conductor - User Manual Verification 'Supervisor Enhancements' (Protocol in workflow.md)

## Phase 3: Final Verification
**Goal:** Confirm the "Single Port" promise and restart stability.

- [ ] Task: Test - Start the server (`make run`) and verify only port 8000 is exposed to the LAN (Copyparty on localhost only).
- [ ] Task: Test - Verify files uploaded via UI appear in `storage/files`.
- [ ] Task: Test - Verify killing Copyparty process results in auto-restart by supervisor.
- [ ] Task: Conductor - User Manual Verification 'Final Verification' (Protocol in workflow.md)
