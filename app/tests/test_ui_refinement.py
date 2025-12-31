import pytest
from pathlib import Path

def test_lightbox_has_refined_layout():
    """Verify that the lightbox template contains the refined header/footer layout."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    assert "lightbox-footer" in content
    assert "lightbox-toolbar" in content
    assert "bi-share" in content
    assert "bi-pencil" in content # Rename
    assert "bi-trash" in content # Delete
    assert "bi-download" in content
    assert "text-center" in content # Centered Title
