import logging
import urllib.parse
import shutil
from fastapi import APIRouter, Request, HTTPException, Depends, Response
from pathlib import Path
from app.core.config import settings
from app.core.file_security import validate_and_resolve_path, is_path_forbidden
from app.core.constants import PREVIEWABLE_EXTENSIONS, VIDEO_EXTENSIONS, TEXT_EXTENSIONS
from app.core.auth import auth_required, decrypt_string
from app.core.templates import templates
from app.backend.services.copyparty_service import get_pmask, get_proxy_headers

router = APIRouter(prefix="/api/v1", dependencies=[Depends(auth_required)])
logger = logging.getLogger(__name__)

@router.delete("/fs/{full_path:path}")
async def delete_file_or_dir(request: Request, full_path: str):
    """
    Deletes a file or directory if the user has 'd' permission.
    """
    base_serve_dir = settings.SERVE_PATH
    
    try:
        full_path = urllib.parse.unquote(full_path)
        resolved_path = validate_and_resolve_path(
            requested_path=Path(full_path),
            base_dir=base_serve_dir,
            client_host=request.client.host
        )

        if not resolved_path.exists():
            raise HTTPException(status_code=404, detail="Path not found")
            
        # Check permissions
        parent_dir = resolved_path.parent.relative_to(base_serve_dir) if resolved_path != base_serve_dir else Path("")
        pmask = get_pmask(request, parent_dir)
        
        logger.info(f"DELETE Request: User='{request.state.session.username if request.state.session else 'anon'}', Path='{resolved_path}', Pmask='{pmask}'")
        
        if 'd' not in pmask:
            logger.warning(f"Delete denied for user in {parent_dir}: Missing 'd' permission in pmask '{pmask}'")
            raise HTTPException(status_code=403, detail="Delete permission denied")

        if resolved_path.is_dir():
            logger.info(f"Deleting directory: {resolved_path}")
            shutil.rmtree(resolved_path)
        else:
            logger.info(f"Deleting file: {resolved_path}")
            resolved_path.unlink()

        # Return empty response for HTMX to remove the element
        return Response(status_code=204)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting {full_path}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/fs/mkdir/{full_path:path}")
async def create_directory(request: Request, full_path: str):
    """
    Creates a new directory if the user has 'w' permission.
    """
    base_serve_dir = settings.SERVE_PATH
    
    try:
        full_path = urllib.parse.unquote(full_path)
        resolved_path = validate_and_resolve_path(
            requested_path=Path(full_path),
            base_dir=base_serve_dir,
            client_host=request.client.host
        )

        if resolved_path.exists():
            raise HTTPException(status_code=400, detail="Directory already exists")
            
        # Check permissions in parent directory
        parent_dir = resolved_path.parent.relative_to(base_serve_dir) if resolved_path != base_serve_dir else Path("")
        pmask = get_pmask(request, parent_dir)
        
        logger.info(f"MKDIR Request: User='{request.state.session.username if request.state.session else 'anon'}', Path='{resolved_path}', Pmask='{pmask}'")
        
        if 'w' not in pmask:
            logger.warning(f"Mkdir denied for user in {parent_dir}: Missing 'w' permission in pmask '{pmask}'")
            raise HTTPException(status_code=403, detail="Write permission denied")

        resolved_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {resolved_path}")

        # Refresh directory listing for HTMX
        contents = sorted(resolved_path.parent.iterdir(), key=lambda f: (not f.is_dir(), f.name.lower()))
        filtered_contents = [item for item in contents if not is_path_forbidden(item)]
        
        context = {
            "request": request,
            "path": str(parent_dir),
            "contents": filtered_contents,
            "pmask": pmask
        }
        
        return templates.TemplateResponse("partials/file_browser_content.html", context)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating directory {full_path}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/gallery/{full_path:path}")
async def get_gallery_metadata(request: Request, full_path: str):
    """
    Returns a list of previewable media files in the same directory as the target path.
    Used for lightbox navigation (Next/Prev).
    """
    base_serve_dir = settings.SERVE_PATH
    
    try:
        # Unquote path to handle spaces from URL
        full_path = urllib.parse.unquote(full_path)
        requested_path = Path(full_path)
        
        # If the path exists and is a file, use its parent. 
        # Otherwise, assume it's a directory.
        actual_path = base_serve_dir / requested_path
        if actual_path.is_file():
            target_dir = requested_path.parent
        else:
            target_dir = requested_path
        
        resolved_dir = validate_and_resolve_path(
            requested_path=target_dir,
            base_dir=base_serve_dir,
            client_host=request.client.host
        )

        if not resolved_dir.is_dir():
            raise HTTPException(status_code=404, detail="Directory not found")

        gallery_items = []
        for item in sorted(resolved_dir.iterdir(), key=lambda f: f.name.lower()):
            if item.is_file() and item.suffix.lower() in PREVIEWABLE_EXTENSIONS:
                if not is_path_forbidden(item):
                    rel_path = item.relative_to(base_serve_dir)
                    
                    item_type = "image"
                    if item.suffix.lower() in VIDEO_EXTENSIONS:
                        item_type = "video"
                    elif item.suffix.lower() in TEXT_EXTENSIONS:
                        item_type = "text"

                    # Encode path parts for URL safety
                    encoded_rel_path = "/".join([urllib.parse.quote(part) for part in rel_path.parts])

                    gallery_items.append({
                        "name": item.name,
                        "path": str(rel_path),
                        "type": item_type,
                        "url": f"/download/{encoded_rel_path}",
                        "thumb": f"/download/{encoded_rel_path}?thumb=300x300"
                    })

        return {
            "current_dir": str(target_dir),
            "pmask": get_pmask(request, target_dir),
            "items": gallery_items
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching gallery metadata for {full_path}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
