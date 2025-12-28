from fastapi.templating import Jinja2Templates
from .config import settings

# Shared templates instance
templates = Jinja2Templates(directory=settings.BASE_DIR / "app" / "frontend" / "templates")
