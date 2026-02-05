import logging
from pathlib import Path
from typing import Optional
from fastapi import HTTPException
from app.core.constants import FORBIDDEN_NAMES, FORBIDDEN_EXTENSIONS
from app.core.config import settings

logger = logging.getLogger(__name__)

def is_path_forbidden(path: Path) -> bool:
    """
    Checks if a given path is forbidden based on its name or extension.
    """
    return path.name in FORBIDDEN_NAMES or path.suffix.lower() in FORBIDDEN_EXTENSIONS

def validate_and_resolve_path(
    requested_path: Path, 
    base_dir: Path,
    client_host: str = "unknown"
) -> Path:
    """
    Resolves a requested path against a base directory and validates it.
    
    This is a critical security function that prevents directory traversal attacks
    by ensuring the final resolved path is safely contained within the intended base directory.
    It raises an HTTPException if validation fails.
    
    Returns:
        The resolved, absolute Path object if valid.
    Raises:
        HTTPException: If the path is invalid or outside the base directory.
    """
    try:
        # Ensure the path is relative to the base_dir
        # We strip leading slashes to prevent absolute path escapes
        safe_requested_path = str(requested_path).lstrip('/')
        
        # Resolve the full path and the base directory to their absolute forms
        resolved_base_dir = base_dir.resolve()
        full_path = (resolved_base_dir / safe_requested_path).resolve()

        # The core security check: Is the resolved path safely within the base directory?
        # We use is_relative_to (Python 3.9+) to ensure the jail is respected.
        if full_path == resolved_base_dir or full_path.is_relative_to(resolved_base_dir):
            if is_path_forbidden(full_path):
                logger.warning(
                    f"[{client_host}] Forbidden access attempt to '{full_path}'"
                )
                raise HTTPException(status_code=404, detail="File not found")
            return full_path
        else:
            logger.warning(
                f"[{client_host}] Path traversal attempt denied: "
                f"'{requested_path}' resolved outside of '{resolved_base_dir}'"
            )
            raise HTTPException(status_code=404, detail="File not found")
            
    except (FileNotFoundError, ValueError):
        # FileNotFoundError from .resolve() if path doesn't exist (sometimes depends on OS)
        # ValueError from .is_relative_to() if paths are on different drives/mounts
        raise HTTPException(status_code=404, detail="File not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.critical(
            f"[{client_host}] Unexpected error during path validation "
            f"for '{requested_path}': {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")

