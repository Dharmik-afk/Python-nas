import logging
import urllib.parse
import shutil
from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Depends, Response
from fastapi.responses import JSONResponse
from pathlib import Path
from app.core.config import settings
from app.core.file_security import validate_and_resolve_path, is_path_forbidden
from app.core.constants import PREVIEWABLE_EXTENSIONS, VIDEO_EXTENSIONS, TEXT_EXTENSIONS
from app.core.auth import auth_required, decrypt_string
from app.core.templates import templates
from app.backend.services.copyparty_service import get_pmask, get_proxy_headers, search_files, rename_item
from app.backend.models.fs_schemas import FSItem, DirectoryListing

router = APIRouter(prefix="/api/v1", dependencies=[Depends(auth_required)])
logger = logging.getLogger(__name__)

@router.get("/fs/list/{full_path:path}", response_model=DirectoryListing)
async def list_directory(request: Request, full_path: str = ""):
    """
    Returns a JSON directory listing for the mobile app.
    """
    base_serve_dir = settings.SERVE_PATH
    
    try:
        full_path = urllib.parse.unquote(full_path)
        resolved_path = validate_and_resolve_path(
            requested_path=Path(full_path),
            base_dir=base_serve_dir,
            client_host=request.client.host
        )

        if not resolved_path.is_dir():
            raise HTTPException(status_code=404, detail="Directory not found")

        pmask = get_pmask(request, Path(full_path))
        
        items = []
        for item in sorted(resolved_path.iterdir(), key=lambda f: (not f.is_dir(), f.name.lower())):
            if not is_path_forbidden(item):
                stat = item.stat()
                rel_path = item.relative_to(base_serve_dir)
                
                # Check permissions for the item itself (if it's a dir, check its pmask)
                # For files, we use the parent's pmask.
                item_pmask = pmask
                if item.is_dir():
                    item_pmask = get_pmask(request, rel_path)

                items.append(FSItem(
                    name=item.name,
                    path=str(rel_path),
                    is_dir=item.is_dir(),
                    size=stat.st_size,
                    mtime=stat.st_mtime,
                    permissions=item_pmask
                ))

        return DirectoryListing(
            path=full_path,
            items=items,
            permissions=pmask
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing directory {full_path}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/fs/search")
async def search(request: Request, q: str = None, format: Optional[str] = None):
    """
    Proxies search request to copyparty.
    Returns transformed JSON if format=json or Accept: application/json is set.
    """
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
    
    results = await search_files(request, q)
    
    accept_header = request.headers.get("accept", "")
    if format == "json" or "application/json" in accept_header:
        hits = results.get("hits", [])
        items = []
        for hit in hits:
            path_str = hit["p"]
            name = path_str.split("/")[-1] or path_str.split("/")[-2] # Handle trailing slash for dirs
            is_dir = path_str.endswith("/")
            
            # For search results, we provide the pmask of the parent or root
            # To be safe and simple for mobile app, we'll return 'r' (read-only) for search hits
            # unless we want to do a full pmask lookup for each hit (expensive).
            items.append(FSItem(
                name=name,
                path=path_str,
                is_dir=is_dir,
                size=hit.get("s", 0),
                mtime=hit.get("t", 0),
                permissions="r" 
            ))
            
        return DirectoryListing(
            path=f"search:{q}",
            items=items,
            permissions="r"
        )
        
    return results

class SearchResultItem:
    def __init__(self, name, path_str):
        self.name = name
        self.path = path_str
        self._is_dir = path_str.endswith("/")
        self.suffix = Path(name).suffix

    def is_file(self):
        return not self._is_dir

    def is_dir(self):
        return self._is_dir

@router.get("/fs/search/ui")
async def search_ui(request: Request, q: str = None, path: str = ""):
    """
    Returns search results as rendered HTML partial.
    If q is empty, returns the normal directory listing for 'path'.
    """
    if not q:
        # Return normal directory listing
        base_serve_dir = settings.SERVE_PATH
        full_path = urllib.parse.unquote(path)
        resolved_path = validate_and_resolve_path(
            requested_path=Path(full_path),
            base_dir=base_serve_dir,
            client_host=request.client.host
        )
        
        if not resolved_path.is_dir():
            raise HTTPException(status_code=404, detail="Directory not found")

        contents = sorted(resolved_path.iterdir(), key=lambda f: (not f.is_dir(), f.name.lower()))
        filtered_contents = [item for item in contents if not is_path_forbidden(item)]
        
        context = {
            "request": request,
            "path": path,
            "contents": filtered_contents,
            "pmask": get_pmask(request, Path(path))
        }
        return templates.TemplateResponse("partials/file_browser_content.html", context)
    
    results = await search_files(request, q)
    hits = results.get("hits", [])
    
    # We need to transform hits into something the template can handle
    # hits: [{"p": "path/to/file", "s": size, "t": mtime}, ...]
    
    transformed_hits = []
    for hit in hits:
        path_str = hit["p"]
        name = path_str.split("/")[-1]
        
        # We'll create a dummy object that mimics a Path object for the template
        transformed_hits.append(SearchResultItem(name, path_str))
    
    context = {
        "request": request,
        "query": q,
        "hits": transformed_hits,
        "pmask": "r", # Search results are usually read-only in this view
        "path": "" # Required by file_card template
    }
    
    return templates.TemplateResponse("partials/search_results.html", context)

@router.post("/fs/rename/{full_path:path}")
async def rename(request: Request, full_path: str, new_name: str = None):
    """
    Renames a file or directory.
    """
    if not new_name:
        raise HTTPException(status_code=400, detail="Query parameter 'new_name' is required")
    
    base_serve_dir = settings.SERVE_PATH
    
    try:
        full_path = urllib.parse.unquote(full_path)
        # Validate source path
        resolved_path = validate_and_resolve_path(
            requested_path=Path(full_path),
            base_dir=base_serve_dir,
            client_host=request.client.host
        )

        if not resolved_path.exists():
            raise HTTPException(status_code=404, detail="Source path not found")
            
        # Check permissions in parent directory
        # Copyparty 'm' permission is required for move/rename
        parent_dir = resolved_path.parent.relative_to(base_serve_dir) if resolved_path != base_serve_dir else Path("")
        pmask = get_pmask(request, parent_dir)
        
        if 'm' not in pmask:
            logger.warning(f"Rename denied for user in {parent_dir}: Missing 'm' permission in pmask '{pmask}'")
            raise HTTPException(status_code=403, detail="Rename permission denied")

        # Perform rename via proxy
        await rename_item(request, Path(full_path), new_name)
        
        logger.info(f"Renamed {full_path} to {new_name}")
        
        # Return success (200 OK)
        # Frontend will likely trigger a reload of the directory
        return JSONResponse(
            content={"status": "success", "message": f"Renamed to {new_name}"},
            headers={"HX-Trigger": '{"show-toast": {"message": "Item renamed successfully", "type": "success"}}'}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error renaming {full_path}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

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
        # Include HX-Trigger for toast notification
        response = Response(status_code=204)
        response.headers["HX-Trigger"] = '{"show-toast": {"message": "Item deleted successfully", "type": "success"}}'
        return response

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
        
        response = templates.TemplateResponse("partials/file_browser_content.html", context)
        response.headers["HX-Trigger"] = '{"show-toast": {"message": "Folder created successfully", "type": "success"}}'
        return response

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
