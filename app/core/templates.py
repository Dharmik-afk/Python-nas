from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.core.config import settings

# Shared templates instance
templates = Jinja2Templates(directory=settings.BASE_DIR / "app" / "frontend" / "templates")

def auth_context(request: Request):
    """
    Injects authentication-related information into the Jinja2 template context.
    """
    session = getattr(request.state, "session", None)
    return {
        "user_permissions": getattr(session, "permissions", "") if session else "",
        "username": getattr(session, "username", "") if session else ""
    }

templates.context_processors.append(auth_context)
