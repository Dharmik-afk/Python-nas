# Implementation Plan: PyPy Runtime Compatibility

## Phase 3: Supervisor & Management Compatibility [checkpoint: 36ae646]
- [x] Task: Write Tests: Verify Supervisor correctly spawns subprocesses using the active PyPy interpreter 75c7961
    - [x] Create a test case that checks the `sys.executable` of spawned child processes.
- [x] Task: Implement: Refactor `supervisor/supervisor.py` for interpreter awareness 75c7961
    - [x] Update `supervisor.py` to use `sys.executable` when launching the FastAPI/Uvicorn process.
    - [x] Ensure that environmental variables (like `VIRTUAL_ENV`) are correctly propagated to child processes.
- [x] Task: Implement: Verify `scripts/manage.py` compatibility 75c7961
    - [x] Test critical management commands (e.g., `list-users`, `add-user`) under PyPy.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Supervisor & Management Compatibility' (Protocol in workflow.md) 36ae646

## Phase 4: Full System Verification & Documentation
- [~] Task: Run full `pytest` suite under CPython (default)
- [ ] Task: Run full `pytest` suite under PyPy (`USE_PYPY=true`)
- [ ] Task: Update `ADMIN_MANUAL.md` or `README.md`
    - [ ] Add a section on "High-Performance Mode (PyPy)".
    - [ ] Document the `USE_PYPY=true` flag and `make setup-pypy` command.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Full System Verification & Documentation' (Protocol in workflow.md)
