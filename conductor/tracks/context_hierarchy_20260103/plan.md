# Plan: AI Context Hierarchy

## Phase 1: Infrastructure & Root Protocol [checkpoint: 7ea9d38]
- [x] Task: Create root `.context/` directory for role-based overlays. 34bc972
- [x] Task: Create initial overlay: `.context/security.md` (extracting security invariants from root `GEMINI.md`). 09c088d
- [x] Task: Update root `GEMINI.md` to include the **Context Loading Protocol** and reference the new system. 674848e
- [x] Task: Conductor - User Manual Verification 'Phase 1: Infrastructure & Root Protocol' (Protocol in workflow.md)

## Phase 2: Context Loader Tooling [checkpoint: 74524e5]
- [x] Task: Create test suite `app/tests/test_context_loader.py` (verifying merge logic and resolution order). 250ed28
- [x] Task: Implement `scripts/context_loader.py` (supporting `--path`, `--task`, and recursive resolution). 250ed28
- [x] Task: Verify tool output format (Markdown with source attribution). 250ed28
- [x] Task: Conductor - User Manual Verification 'Phase 2: Context Loader Tooling' (Protocol in workflow.md)

## Phase 3: Modularization & Scoping
- [x] Task: Create `app/backend/.context.md` (scoped backend rules and FastAPI/SQLAlchemy details). 23903aa
- [x] Task: Create `app/frontend/.context.md` (scoped frontend/HTMX/Alpine.js rules). 8b523bb
- [x] Task: Create `app/tests/.context.md` (scoped testing guidelines and coverage targets). fc0ef83
- [x] Task: Create `scripts/.context.md` (scoped operational/automation rules). 4493afe
- [~] Task: Conductor - User Manual Verification 'Phase 3: Modularization & Scoping' (Protocol in workflow.md)

## Phase 4: Integration & Documentation
- [ ] Task: Refactor root `GEMINI.md` to remove redundant modular info (keeping only global/core context).
- [ ] Task: Update `DEBUG.md` with maintenance instructions for the context hierarchy.
- [ ] Task: Final end-to-end verification (Agent successfully uses loader to resolve deep context).
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Integration & Documentation' (Protocol in workflow.md)
