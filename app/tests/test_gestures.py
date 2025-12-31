import pytest
from pathlib import Path

def test_lightbox_has_content_aware_gestures():
    """Verify that the lightbox template contains content-aware gesture logic."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    assert "Math.abs(diffY) > Math.abs(diffX)" in content
    assert "verticalThreshold" in content
    assert "150" in content # Check for increased threshold
    assert "this.close()" in content # Vertical swipe close
    assert "Document Isolation" in content
    assert "item.type === 'text'" in content
    assert "item.type === 'image' || item.type === 'video'" in content
