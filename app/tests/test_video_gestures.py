import pytest
from pathlib import Path

def test_lightbox_has_video_gestures():
    """Verify that the lightbox template contains video gesture logic."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    assert "handleTouchStart" in content
    assert "handleTouchMove" in content
    assert "isAdjustingVolume" in content
    assert "isAdjustingBrightness" in content
    assert "brightnessLevel" in content
    assert "bi-brightness-high-fill" in content
    assert "bi-volume-up-fill" in content
