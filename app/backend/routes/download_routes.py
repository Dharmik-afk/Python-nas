import logging
from fastapi import APIRouter, Request, HTTPException, Depends
from pathlib import Path

from app.core.config import settings
from app.core.file_security import validate_and_resolve_path
from app.backend.services import copyparty_service
from app.core.metrics import metrics
from app.core.auth import auth_required

router = APIRouter(dependencies=[Depends(auth_required)])
logger = logging.getLogger(__name__)

@router.get("/download/{full_path:path}", tags=["Mobile API"], summary="Stream or download a file")
async def download_file(request: Request, full_path: str):
    """
    Proxies a file download or media request to the copyparty backend.
    Supports query parameters for thumbnails (?thumb=WxH) and Range headers for video streaming.
    """
    logger.info(f"File request received for path: {full_path}")
    base_serve_dir = settings.SERVE_PATH
    
    try:
        resolved_path = validate_and_resolve_path(
            requested_path=Path(full_path),
            base_dir=base_serve_dir,
            client_host=request.client.host
        )

        if resolved_path.is_file():
            relative_path = resolved_path.relative_to(base_serve_dir)
            
            # Capture query parameters (e.g., ?thumb=300x300 or ?media)
            query_params = dict(request.query_params)
            
            # Capture relevant headers (especially 'range' for video players)
            client_headers = {k.lower(): v for k, v in request.headers.items()}
            
            session = getattr(request, "state", None) and getattr(request.state, "session", None)
            if session:
                logger.debug(f"Download route: Active session for user '{session.username}'")
            else:
                logger.warning("Download route: No active session found in request.state")

            logger.debug(f"Proxying request for: {relative_path} with params: {query_params}")
            metrics.record_download()
            
            return await copyparty_service.proxy_stream_request(
                request=request,
                relative_path=relative_path,
                params=query_params,
                request_headers=client_headers
            )
        else:
            logger.warning(f"Request for non-file path: {resolved_path}")
            raise HTTPException(status_code=404, detail="Path is not a file")

    except HTTPException:
        # Re-raise HTTPException directly to preserve status code and detail
        raise
    except Exception as e:
        logger.error(f"Unexpected error during download for path '{full_path}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")