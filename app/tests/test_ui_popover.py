import pytest
from pathlib import Path

def test_lightbox_popover_structure():
    """Verify that the lightbox uses a popover for details instead of a bottom sheet."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    assert "lightbox-popover" in content
    assert "@click.outside" in content
    assert "bottom-sheet" not in content # Ensure old markup is gone
    assert "detail-icon" in content
    assert "x-transition:enter" in content # Ensure animation is present
