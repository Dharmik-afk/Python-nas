import logging
from fastapi import APIRouter, Request, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.core.config import settings
from app.core.file_security import validate_and_resolve_path, is_path_forbidden
from app.core.metrics import metrics
from app.core.templates import templates
from app.backend.services.copyparty_service import get_pmask

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/api/v1/stats")
async def get_server_stats():
    """Returns real-time server metrics."""
    return metrics.get_stats()

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Renders the login page."""
    return templates.TemplateResponse("pages/login.html", {"request": request})

@router.get("/video-test", response_class=HTMLResponse)
async def video_test(request: Request):
    """A test route for the new custom video player."""
    # We need a dummy item for the partial to work
    # In a real environment, the user can test this with an actual video file
    dummy_item = {
        "url": "/download/test.mp4",
        "name": "Test Video"
    }
    return templates.TemplateResponse("pages/video_test.html", {"request": request, "currentItem": dummy_item})

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return await read_path(request, "")

@router.get("/{full_path:path}", response_class=HTMLResponse)
async def read_path(request: Request, full_path: str):
    """
    Handles browsing of files and directories.
    """
    # Force login for all routes except /login and static files
    session = getattr(request.state, "session", None)
    if not session or not session.auth_header:
        if "HX-Request" in request.headers:
            return Response(headers={"HX-Redirect": "/login"})
        return RedirectResponse(url="/login")

    base_serve_dir = settings.SERVE_PATH
    logger.info(f"Request for path: '{full_path}'")
    logger.debug(f"Serving from base directory: {base_serve_dir}")
    
    try:
        resolved_path = validate_and_resolve_path(
            requested_path=Path(full_path),
            base_dir=base_serve_dir,
            client_host=request.client.host
        )
        logger.debug(f"Resolved path to: '{resolved_path}'")
        logger.debug(f"Path properties: exists={resolved_path.exists()}, is_dir={resolved_path.is_dir()}, is_file={resolved_path.is_file()}")

        if resolved_path.is_dir():
            logger.debug("Path is a directory, preparing to list contents.")
            try:
                contents = sorted(resolved_path.iterdir(), key=lambda f: (not f.is_dir(), f.name.lower()))
            except PermissionError:
                logger.warning(f"Permission denied for directory: {resolved_path}")
                raise HTTPException(status_code=403, detail="Permission denied")

            filtered_contents = [item for item in contents if not is_path_forbidden(item)]
            logger.debug(f"Found {len(filtered_contents)} items to display.")

            # Determine which template to render based on the request headers
            is_htmx_request = "HX-Request" in request.headers
            template_name = "partials/file_browser_content.html" if is_htmx_request else "pages/file_browser.html"
            logger.debug(f"Rendering template: '{template_name}' (htmx_request={is_htmx_request})")
            
            context = {
                "request": request,
                "path": full_path,
                "contents": filtered_contents,
                "pmask": get_pmask(request, full_path if isinstance(full_path, Path) else Path(full_path))
            }
            return templates.TemplateResponse(template_name, context)

        elif resolved_path.is_file():
            logger.debug(f"Path is a file: {resolved_path.name}. Redirecting to download.")
            return RedirectResponse(url=f"/download/{full_path}")

    except HTTPException as e:
        logger.error(f"HTTP Exception for path '{full_path}': {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error for path '{full_path}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

    # This part of the code should ideally not be reached
    logger.warning(f"No content returned for path: {full_path}")
    raise HTTPException(status_code=404, detail="Path not found")
