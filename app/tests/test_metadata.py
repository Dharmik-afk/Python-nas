import pytest
from pathlib import Path

def test_lightbox_metadata_extraction():
    """Verify that the lightbox template contains metadata extraction logic."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    # State initialization
    assert "mediaMetadata: { width: null" in content
    
    # Image extraction
    assert "extractImageMetadata($event.target)" in content
    assert "img.naturalWidth" in content
    
    # Video extraction
    assert "vid.videoWidth" in content
    assert "vid.videoHeight" in content
    
    # UI Binding
    assert "x-text=\"mediaMetadata.width + ' x ' + mediaMetadata.height\"" in content

