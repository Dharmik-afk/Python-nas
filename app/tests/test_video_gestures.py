import pytest
from pathlib import Path

def test_lightbox_has_video_gestures():
    """Verify that the lightbox template contains video gesture logic."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    assert "handleVideoTouchStart" in content
    assert "handleVideoTouchMove" in content
    assert "isAdjustingVolume" in content
    assert "flex-column-reverse" in content # Fix for upside down meters
    assert "playing ? 'bottom: 0;' : 'bottom: 80px;'" in content # Progress bar positioning
    assert "isAdjustingBrightness" in content
    assert "brightnessLevel" in content
    assert "bi-brightness-high-fill" in content
    assert "bi-volume-up-fill" in content
