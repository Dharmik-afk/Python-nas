import logging
from fastapi import APIRouter, UploadFile, File, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from typing import List
from pathlib import Path

from app.core.config import settings
from app.core.file_security import validate_and_resolve_path, is_path_forbidden
from app.backend.services.copyparty_service import proxy_upload_request
from app.core.metrics import metrics
from app.core.templates import templates
from app.core.auth import auth_required

router = APIRouter(dependencies=[Depends(auth_required)])
logger = logging.getLogger(__name__)

@router.post("/upload/{full_path:path}")
async def upload_files(
    request: Request,
    full_path: str,
    files: List[UploadFile] = File(...)
):
    """
    Handles file uploads to a specific directory.
    Proxies the upload to the copyparty backend.
    Returns the updated file list (HTMX partial).
    """
    base_serve_dir = settings.SERVE_PATH
    logger.info(f"Upload request for path: '{full_path}' with {len(files)} files")
    
    try:
        resolved_path = validate_and_resolve_path(
            requested_path=Path(full_path),
            base_dir=base_serve_dir,
            client_host=request.client.host if request.client else "unknown"
        )
        
        if not resolved_path.is_dir():
            raise HTTPException(status_code=400, detail="Target path is not a directory.")

        success_count = 0
        for file in files:
            # Basic check for forbidden filenames before sending to backend
            if is_path_forbidden(Path(file.filename)):
                logger.warning(f"Skipping forbidden filename: {file.filename}")
                continue
                
            try:
                # Calculate the relative path within the SERVE_DIR to avoid absolute path nesting in backend
                relative_target_dir = resolved_path.relative_to(base_serve_dir)
                
                if proxy_upload_request(request, relative_target_dir, file):
                    success_count += 1
                    metrics.record_upload()
            except Exception as e:
                logger.error(f"Failed to upload {file.filename}: {e}")
                # Continue uploading other files? Or fail?
                # For now, log and continue.

        logger.info(f"Successfully uploaded {success_count}/{len(files)} files.")

        # Refresh directory listing
        contents = sorted(resolved_path.iterdir(), key=lambda f: (not f.is_dir(), f.name.lower()))
        filtered_contents = [item for item in contents if not is_path_forbidden(item)]
        
        context = {
            "request": request,
            "path": full_path,
            "contents": filtered_contents,
        }
        
        # Return the updated file grid
        return templates.TemplateResponse("partials/file_browser_content.html", context)

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during upload: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error during upload.")
