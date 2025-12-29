import logging
from pathlib import Path
from typing import Optional
from fastapi import HTTPException
from .constants import FORBIDDEN_NAMES, FORBIDDEN_EXTENSIONS
from .config import settings

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
        full_path = (base_dir / requested_path).resolve()
        resolved_base_dir = base_dir.resolve()

        # Global Security Check: Enforce Restricted Directories
        for restricted in settings.RESTRICTED_DIRS:
            # Check if the path is inside a restricted directory
            # We use try/except because is_relative_to can fail on different drives (mostly Windows, but safe to handle or just ignore)
            # On Linux/Android it should be fine.
            try:
                if full_path.is_relative_to(restricted):
                    # It is restricted, unless it is in an allowed override
                    is_exempt = False
                    for allowed in settings.ALLOWED_OVERRIDE_DIRS:
                        if full_path.is_relative_to(allowed):
                            is_exempt = True
                            break
                    
                    if not is_exempt:
                        logger.warning(
                            f"[{client_host}] Access denied: '{full_path}' is in a restricted system directory '{restricted}'"
                        )
                        raise HTTPException(status_code=404, detail="File not found")
            except ValueError:
                continue # Not relative to this restricted path

        # The core security check: Is the resolved path safely within the base directory?
        if full_path.is_relative_to(resolved_base_dir):
            if is_path_forbidden(full_path):
                logger.warning(
                    f"[{client_host}] Forbidden access attempt to '{full_path}'"
                )
                raise HTTPException(status_code=404, detail="File not found")
            return full_path
        else:
            logger.warning(
                f"[{client_host}] Path traversal attempt denied: "
                f"'{requested_path}' resolved outside of '{base_dir}'"
            )
            raise HTTPException(status_code=404, detail="File not found")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.critical(
            f"[{client_host}] Unexpected error during path validation "
            f"for '{requested_path}': {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")

