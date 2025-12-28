import logging
from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from .core.config import settings
from .core.logger import setup_logging
from .core.utils import get_lan_ip
from .core.session_manager import session_manager
from .core.user_sync import sync_users_to_copyparty
from app.backend.routes import download_routes, upload_routes, api_routes, auth_routes
from app.frontend.routes import frontend_routes

app = FastAPI(title="Python File Server")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Validation error for {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": str(exc.body)},
    )

# Mount static files (CSS, JS, Images)
app.mount("/static", StaticFiles(directory=settings.BASE_DIR / "app" / "frontend" / "static"), name="static")

@app.middleware("http")
async def session_middleware(request: Request, call_next):
    # Skip session handling for static files and favicon to save resources
    if request.url.path.startswith("/static") or request.url.path == "/favicon.ico":
        return await call_next(request)

    session_id = request.cookies.get("session_id")
    session = None
    if session_id:
        session = session_manager.get_session(session_id)
    
    new_session_id = None
    if not session:
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        session = session_manager.create_session(client_ip, user_agent)
        new_session_id = session.session_id
    
    # Store session in request state for endpoints to use
    request.state.session = session
    
    # Log activity (simple path logging)
    if session:
        session.log_activity(f"Requested {request.url.path}")

    response = await call_next(request)
    
    # Persist session changes (like login status) only if needed
    if session and session.modified:
        session_manager.save_sessions()
        session.modified = False

    if new_session_id:
        response.set_cookie(
            key="session_id",
            value=new_session_id,
            httponly=True,
            samesite="lax",
            secure=False,
            max_age=settings.SESSION_TIMEOUT_SECONDS
        )
    
    return response

@app.on_event("startup")
async def startup_event():
    """
    Actions to perform on application startup.
    """
    setup_logging()
    
    # Determine the IP for the user-facing message
    host_ip = get_lan_ip()
    
    logging.info(f"FastAPI Worker starting...")
    logging.info(f"Serving files from: {settings.SERVE_DIR}")
    
    if host_ip.startswith("127."):
        logging.warning("Note: Network Access IP is loopback. Ensure your device is connected to a network.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to perform on application shutdown.
    """
    logging.info("FastAPI Worker shutting down...")

# Include the router for handling file downloads
app.include_router(download_routes.router)
# Include the router for handling file uploads
app.include_router(upload_routes.router)
# Include the API router
app.include_router(api_routes.router)
# Include the Auth router
app.include_router(auth_routes.router)
@app.get("/health")
async def health_check():
    """Health check endpoint for the supervisor."""
    return {"status": "ok"}

# Include the router for serving HTML pages and handling frontend interactions
# This must be included last because it contains a catch-all route
app.include_router(frontend_routes.router)

