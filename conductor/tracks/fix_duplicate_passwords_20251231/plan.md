# Implementation Plan: Fix Duplicate Password Limitation in Copyparty Integration

This plan addresses the "duplicate password" error by ensuring password hashes are unique per user using standard salting techniques, primarily focusing on the `passlib` configuration and the `user_sync` logic.

## Phase 1: Reproduce and Diagnose (Red Phase) [checkpoint: fef5a1a]
- [x] Task: Create a reproduction script or test in `app/tests/test_duplicate_passwords.py`.
- [x] Task: Verify that creating two users with the same password and attempting login triggers the `copyparty` error.
- [x] Task: Analyze current hashing implementation in `app/core/security.py` and `scripts/manage.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Reproduce and Diagnose' (Protocol in workflow.md) e011587

## Phase 2: Implement Salted Hashing (Green Phase) [checkpoint: 09bfe07]
- [x] Task: Update `app/core/security.py` to use a more robust hashing configuration if not already present (ensure `passlib` is handling salts correctly).
- [x] Task: Modify `app/core/user_sync.py` to ensure that the hashes sent to `copyparty.conf` are generated in a way that Copyparty accepts them as unique (e.g., using Copyparty's supported salted formats).
- [x] Task: Update `scripts/manage.py` to use the updated hashing logic when adding users via the CLI.
- [x] Task: Verify that the reproduction test now passes (two users with same password can coexist).
- [x] Task: Conductor - User Manual Verification 'Phase 2: Implement Salted Hashing' (Protocol in workflow.md) 4778a7b

## Phase 3: Migration and Cleanup [checkpoint: ff6315c]
- [x] Task: Implement a check to handle legacy (unsalted) hashes for existing users if necessary, or decide on a re-hash strategy.
- [x] Task: Perform a final verification with `make add-user` and manual login for two identical-password accounts.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Migration and Cleanup' (Protocol in workflow.md) d187350
