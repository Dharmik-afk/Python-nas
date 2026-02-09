# Specification: Comprehensive Codebase Context Audit

## Overview
This chore involves a systematic review of the project's source code and infrastructure to generate and maintain a hierarchical context system. The goal is to create local `.context.md` files in sub-directories and a centralized `CONTEXT.md` in the root that serves both as an aggregator and the primary documentation for root-level components.

## Scope
- **Source Code:** All directories and files within the `app/` directory.
- **Infrastructure & Configuration:** Root-level files (e.g., `Makefile`, `package.json`, `pyproject.toml`, `main.py`, `alembic.ini`) and the `alembic/` migration directory.
- **Exclusions:** External dependencies (`.venv/`, `.venv-pypy/`, `node_modules/`) and temporary build/test artifacts.

## Functional Requirements

### 1. Local Context Generation (`.context.md`)
For every **sub-directory** within the scope (e.g., `app/core/`, `alembic/`), a `.context.md` file must be created or updated. Each file must include:
- **Purpose & Responsibility:** A high-level summary of the directory's role in the system.
- **Key Symbols:** A list of the most important classes, functions, or variables defined in that directory and their specific roles.
- **Dependencies:** A list of internal and external dependencies relevant to the code within that directory.

### 2. Root Context Management (`CONTEXT.md`)
A centralized `CONTEXT.md` file must be maintained in the project root.
- **For Sub-directories:** It should follow a "Summary & Link" pattern (high-level summary + link to the local `.context.md`).
- **For Root Files:** It must contain the full detailed context (Purpose, Key Symbols, Dependencies) for each infrastructure or code file located directly in the root (e.g., `Makefile`, `main.py`).
- **Synchronization:** The root file must be updated whenever a local `.context.md` is created or modified, or when a root-level file is audited.

### 3. Execution Process
- The auditor must read files "one by one" (systematically) to ensure accurate data collection.
- Context should be captured for existing logic, patterns, and architectural decisions.

## Non-Functional Requirements
- **Consistency:** All context entries should follow a uniform internal structure for readability.
- **Accuracy:** The findings must reflect the actual state of the code.

## Acceptance Criteria
- [ ] Every sub-directory in `app/` and `alembic/` contains a `.context.md` file.
- [ ] The root `CONTEXT.md` contains full detailed context for all root-level infrastructure and code files.
- [ ] The root `CONTEXT.md` provides summaries and links for all local context files.
