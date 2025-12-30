import pytest
from pathlib import Path

def test_lightbox_template_has_prefetch_logic():
    """Verify that the lightbox template contains prefetching logic."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    # These terms should be present after implementation
    assert "prefetch" in content
    assert "prefetchAdjacent" in content
    assert "const nextIndex = (this.currentIndex + 1)" in content
