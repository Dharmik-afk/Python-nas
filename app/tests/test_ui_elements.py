import pytest
from pathlib import Path

def test_lightbox_has_google_photos_ui():
    """Verify that the lightbox template contains Google Photos inspired UI elements."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    assert "btn-glass" in content
    assert "bottom-sheet" in content
    assert "showDetails" in content
    assert "toggleDetails()" in content
    assert "detail-item" in content
