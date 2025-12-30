import logging
import requests
from fastapi import HTTPException, UploadFile, Request
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask
from pathlib import Path

from app.core.config import settings
from app.core.auth import decrypt_string

logger = logging.getLogger(__name__)

def get_user_permissions_from_config(username: str) -> str:
    """
    Parses copyparty/copyparty.conf to retrieve the user's permission mask 
    for the root volume.
    """
    conf_path = settings.BASE_DIR / "copyparty" / "copyparty.conf"
    if not conf_path.exists():
        logger.warning(f"Copyparty config not found at {conf_path}")
        return ""

    try:
        with open(conf_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line.startswith("-v "):
                    continue
                
                # Format: -v src:dst:perm1,u1,u2:perm2,u3
                parts = line.split(":")
                if len(parts) < 3:
                    continue
                
                # Destination must be root '/'
                if parts[1] != "/":
                    continue
                
                # Check each permission group (starting from index 2)
                for group in parts[2:]:
                    # Group format: perms,user1,user2...
                    sub_parts = group.split(",")
                    if len(sub_parts) < 2:
                        continue
                    
                    perms = sub_parts[0]
                    users = sub_parts[1:]
                    if username in users:
                        logger.info(f"Parsed permissions for '{username}' from config: {perms}")
                        return perms
        
        logger.warning(f"User '{username}' not found in any root volume in {conf_path}")
        return ""
    except Exception as e:
        logger.error(f"Error parsing copyparty.conf: {e}")
        return ""

def get_user_permissions(username: str, password: str) -> str:
    """
    DEPRECATED: Use get_user_permissions_from_config instead.
    Kept for compatibility during transition.
    """
    return get_user_permissions_from_config(username)

def _get_proxy_url(relative_path: Path) -> str:
    """Constructs the full URL to proxy a request to the copyparty backend."""
    url_path = str(relative_path.as_posix()).lstrip('/')
    proxy_url = f"http://127.0.0.1:{settings.COPYPARTY_PORT}/{url_path}"
    return proxy_url

def get_proxy_headers(request: Request) -> dict:
    """Constructs the necessary headers for proxying, using current user credentials."""
    session = getattr(request.state, "session", None)
    client_host = request.client.host if request.client else "unknown"
    
    headers = {
        "User-Agent": "FastAPI-Proxy/1.0",
        "X-Real-IP": client_host
    }
    
    if session:
        logger.debug(f"Session found for user: {session.username}")
        if session.auth_header:
            decrypted_auth = decrypt_string(session.auth_header)
            if decrypted_auth:
                headers["Authorization"] = decrypted_auth
                logger.debug(f"Authorization header set (masked): {decrypted_auth[:15]}...")
            else:
                logger.warning(f"Auth header decryption returned empty string for user: {session.username}")
        else:
            logger.warning(f"Session found but NO auth_header for user: {session.username}")
    else:
        logger.warning(f"No active session found for request from {client_host}")
    
    return headers

def proxy_upload_request(request: Request, relative_path: Path, file: UploadFile) -> bool:
    """Proxies a file upload request to the copyparty backend via PUT."""
    if not file.filename:
        logger.error("Upload request with missing filename.")
        raise HTTPException(status_code=400, detail="Filename is required.")

    target_url = _get_proxy_url(relative_path / Path(file.filename))
    headers = get_proxy_headers(request)
    
    logger.info(f"Proxying upload of '{file.filename}' to {target_url}")

    try:
        r = requests.put(target_url, headers=headers, data=file.file, timeout=3600)
        r.raise_for_status()
        logger.info(f"Upload successful: {r.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Proxy upload failed for '{file.filename}': {e}")
        raise HTTPException(status_code=502, detail=f"Backend upload failed: {str(e)}")

async def proxy_api_request(request: Request, relative_path: Path, params: dict = None) -> dict:
    """Proxies a request to the copyparty backend expecting a JSON response."""
    url = _get_proxy_url(relative_path)
    headers = get_proxy_headers(request)
    headers["Accept"] = "application/json"

    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Proxy API request failed: {e}")
        raise HTTPException(status_code=502, detail=f"Backend API failed: {str(e)}")

async def proxy_post_request(request: Request, relative_path: Path, params: dict = None, data: dict = None) -> bool:
    """Proxies a POST request to the copyparty backend."""
    url = _get_proxy_url(relative_path)
    headers = get_proxy_headers(request)
    
    try:
        r = requests.post(url, headers=headers, params=params, data=data, timeout=10)
        r.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Proxy POST request failed: {e}")
        raise HTTPException(status_code=502, detail=f"Backend POST failed: {str(e)}")

async def search_files(request: Request, query: str, relative_path: Path = Path("")) -> dict:
    """
    Performs a recursive search using the copyparty backend.
    """
    params = {
        "q": query,
        "json": ""  # Copyparty uses &json to return JSON results
    }
    return await proxy_api_request(request, relative_path, params=params)

async def rename_item(request: Request, relative_path: Path, new_name: str) -> bool:
    """
    Renames a file or directory using copyparty's move API.
    """
    # The 'move' parameter expects the full destination path
    # relative to the volume root.
    parent_dir = relative_path.parent
    new_path = parent_dir / new_name
    
    # Copyparty API: POST /src?move=/dst
    params = {
        "move": "/" + str(new_path.as_posix()).lstrip('/')
    }
    
    return await proxy_post_request(request, relative_path, params=params)

def get_pmask(request: Request, relative_path: Path) -> str:
    """Fetches the permission mask for the current user in the target directory."""
    url = _get_proxy_url(relative_path)
    # Manually append ?pmask to ensure it is sent as a flag, not a key-value pair
    if "?" in url:
        url += "&pmask"
    else:
        url += "?pmask"
        
    headers = get_proxy_headers(request)
    
    # Log the attempt
    session = getattr(request.state, "session", None)
    username = session.username if session else "anonymous"
    logger.debug(f"Querying pmask for user '{username}' at '{url}'")

    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            pmask = r.text.strip()
            # Validate that we didn't get an HTML error page or directory listing
            if pmask.lower().startswith("<!doctype") or "<html" in pmask.lower():
                logger.error(f"Received HTML response instead of pmask for '{username}'. Response starts with: {pmask[:50]}")
                # Fallback required
            else:
                logger.info(f"Retrieved pmask for '{username}': '{pmask}'")
                return pmask
        else:
             logger.warning(f"Backend pmask request returned {r.status_code}, falling back to session permissions.")

    except Exception as e:
        logger.error(f"Failed to fetch pmask for {relative_path}: {e}, falling back to session permissions.")
    
    # Fallback to session permissions if backend is unreachable or returns error
    if session and session.permissions:
        logger.info(f"Falling back to session permissions for '{username}': {session.permissions}")
        return session.permissions
        
    return "r"

async def proxy_stream_request(request: Request, relative_path: Path, params: dict = None, request_headers: dict = None):
    """Proxies a file download or directory zip request to the copyparty backend."""
    url = _get_proxy_url(relative_path)
    headers = get_proxy_headers(request)
    
    clean_params = {k: v for k, v in params.items()} if params else {}

    if request_headers:
        for header in ['range', 'if-range', 'if-match', 'if-none-match', 'if-modified-since', 'if-unmodified-since']:
            if header in request_headers:
                headers[header] = request_headers[header]

    try:
        logger.debug(f"--- PROXY REQUEST START ---")
        logger.debug(f"Target URL: {url}")
        
        # Log headers (masking sensitive info)
        debug_headers = headers.copy()
        if "Authorization" in debug_headers:
            debug_headers["Authorization"] = debug_headers["Authorization"][:15] + "..."
        logger.debug(f"Request Headers: {debug_headers}")
        
        # Use stream=True for large files
        r = requests.get(url, headers=headers, params=clean_params, stream=True, timeout=3600)
        
        logger.debug(f"Response Status: {r.status_code}")
        logger.debug(f"Response Headers: {dict(r.headers)}")

        if r.status_code >= 400:
            error_content = r.text[:500]
            logger.error(f"Backend returned error {r.status_code}: {error_content}")
            raise HTTPException(status_code=r.status_code, detail=f"Backend error: {r.status_code}")

        task = BackgroundTask(r.close)
        
        excluded_headers = ['connection', 'keep-alive', 'transfer-encoding', 'server', 'date', 'content-disposition']
        response_headers = {k: v for k, v in r.headers.items() if k.lower() not in excluded_headers}
        
        is_preview = params and ('thumb' in params or 'media' in params)
        filename = relative_path.name
        
        if is_preview:
            response_headers["Content-Disposition"] = f'inline; filename="{filename}"'
        else:
            response_headers["Content-Disposition"] = f'attachment; filename="{filename}"'

        return StreamingResponse(
            r.iter_content(chunk_size=128 * 1024),
            status_code=r.status_code,
            headers=response_headers,
            media_type=r.headers.get('Content-Type'),
            background=task
        )

    except requests.exceptions.RequestException as e:
        logger.error(f"Proxy request to copyparty failed: {e}")
        raise HTTPException(status_code=502, detail="Bad Gateway: Could not connect to backend file server.")