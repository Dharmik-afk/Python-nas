# Implementation Plan: Fix Unicode Encoding in Video Streaming Headers

This plan addresses the `UnicodeEncodeError` in `StreamingResponse` by ensuring headers passed from `copyparty_service` to FastAPI are properly sanitized and encoded.

## Phase 1: Reproduce and Validate (Red Phase) [checkpoint: 352f596]
- [x] Task: Create a reproduction test case in `app/tests/test_download_unicode.py`.
- [x] Task: Verify that the test fails with `UnicodeEncodeError` when using a filename with non-ASCII characters (e.g., `Boys പൊളിയാ.mp4`).
- [x] Task: Conductor - User Manual Verification 'Phase 1: Reproduce and Validate' (Protocol in workflow.md) b41808f

## Phase 2: Implementation (Green Phase) [checkpoint: 1f6c8cf]
- [x] Task: Modify `app/backend/services/copyparty_service.py` to sanitize headers.
    - [x] Sub-task: Identify headers containing non-ASCII characters (e.g., `Set-Cookie`, `Content-Disposition`).
    - [x] Sub-task: Implement a helper to URL-encode or remove problematic characters from sensitive headers before passing them to `StreamingResponse`.
- [x] Task: Update `app/backend/routes/download_routes.py` if necessary to handle character encoding in the response.
- [x] Task: Verify that the reproduction test now passes.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Implementation' (Protocol in workflow.md) afeb0a5

## Phase 3: Refinement and Verification [checkpoint: 61294e3]
- [x] Task: Ensure `Content-Disposition` header correctly uses `filename*=` (RFC 5987) for non-ASCII filenames so browsers download them with the correct name.
- [x] Task: Run full suite of download and streaming tests (`app/tests/test_copyparty_service.py`, `app/tests/test_api.py`) to ensure no regressions.
- [ ] Task: Verify fix on a real device/browser with the specific "SSYdance" video file or a similar dummy file with Malayalam characters.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Refinement and Verification' (Protocol in workflow.md) fd0dd40
