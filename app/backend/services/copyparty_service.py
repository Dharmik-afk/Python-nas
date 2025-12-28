import logging
import requests
from fastapi import HTTPException, UploadFile, Request
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask
from pathlib import Path

from app.core.config import settings
from app.core.auth import decrypt_string

logger = logging.getLogger(__name__)

def _get_proxy_url(relative_path: Path) -> str:
    """Constructs the full URL to proxy a request to the copyparty backend."""
    url_path = str(relative_path.as_posix()).lstrip('/')
    proxy_url = f"http://127.0.0.1:{settings.COPYPARTY_PORT}/{url_path}"
    return proxy_url

def _get_proxy_headers(request: Request) -> dict:
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
    headers = _get_proxy_headers(request)
    
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
    headers = _get_proxy_headers(request)
    headers["Accept"] = "application/json"

    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Proxy API request failed: {e}")
        raise HTTPException(status_code=502, detail=f"Backend API failed: {str(e)}")

def get_pmask(request: Request, relative_path: Path) -> str:
    """Fetches the permission mask for the current user in the target directory."""
    url = _get_proxy_url(relative_path)
    headers = _get_proxy_headers(request)
    params = {"pmask": None}

    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        return r.text.strip()
    except Exception as e:
        logger.error(f"Failed to fetch pmask for {relative_path}: {e}")
        return "r"

async def proxy_stream_request(request: Request, relative_path: Path, params: dict = None, request_headers: dict = None):
    """Proxies a file download or directory zip request to the copyparty backend."""
    url = _get_proxy_url(relative_path)
    headers = _get_proxy_headers(request)
    
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