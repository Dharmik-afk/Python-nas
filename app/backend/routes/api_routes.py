import logging
import urllib.parse
from fastapi import APIRouter, Request, HTTPException, Depends
from pathlib import Path
from app.core.config import settings
from app.core.file_security import validate_and_resolve_path, is_path_forbidden
from app.core.constants import PREVIEWABLE_EXTENSIONS, VIDEO_EXTENSIONS, TEXT_EXTENSIONS
from app.core.auth import auth_required, decrypt_string
from app.backend.services.copyparty_service import get_pmask

router = APIRouter(prefix="/api/v1", dependencies=[Depends(auth_required)])
logger = logging.getLogger(__name__)

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
