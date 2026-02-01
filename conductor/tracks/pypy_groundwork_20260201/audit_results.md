# Dependency Audit for PyPy 3.12 Compatibility

**Date:** 2026-02-01
**Target Runtime:** PyPy 3.12
**System:** Android (Termux)

## Overview
This document records the compatibility audit of the project's dependencies defined in `pyproject.toml` against the PyPy 3.12 runtime.

## Critical Dependencies

| Package | Version | PyPy Support | Notes |
| :--- | :--- | :--- | :--- |
| **fastapi** | 0.99.1 | ✅ Compatible | Pure Python. |
| **pydantic** | 1.10.26 | ✅ Compatible | V1.10 has good compatibility. Performance may be lower than CPython without compiled extensions, but functional. |
| **sqlalchemy** | 2.0.45 | ✅ Compatible | Supports PyPy. C-extensions for speedups might not build, but pure Python fallback exists. |
| **greenlet** | 3.3.0 | ⚠️ Check Required | Required for SQLAlchemy asyncio. PyPy often includes its own greenlet or requires a specific build. `greenlet >= 3.0` generally supports PyPy 3.10+, need to verify 3.12 specific wheels or buildability. |
| **uvicorn** | 0.40.0 | ✅ Compatible | Standard implementation is compatible. We are not using `uvloop`, so no conflict there. |
| **cffi** | 2.0.0 | ✅ Native | PyPy is built on CFFI. This is a core component. |

## Potential Build Requirements (Termux)
The following packages may require `clang` and `make` to build from source during `uv sync` if pre-built wheels are not available for the `aarch64` + `PyPy` combination:

*   `greenlet`
*   `markupsafe` (Speedups)
*   `cffi` (If updating)
*   `sqlalchemy` (Speedups)

## Strategy
1.  Attempt `uv sync` with `pypy3.12`.
2.  Allow fallbacks to pure Python wheels where applicable.
3.  Monitor `greenlet` installation closely as it is critical for `anyio`/`sqlalchemy` async interactions.

## Conclusion
The dependency tree appears largely compatible. No hard blockers (like `numpy` or complex scientific stacks) are present. The main risk is compilation failures for optional speedups on Termux.
