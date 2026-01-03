import pytest
from pathlib import Path

def test_artplayer_loading_icon_configured():
    """Verify that Artplayer is configured with a custom loading spinner."""
    lightbox_path = Path("app/frontend/templates/partials/lightbox.html")
    content = lightbox_path.read_text()
    
    # Check for the icons.loading configuration
    assert "icons: {" in content
    assert "loading:" in content
    assert "spinner-border" in content
    assert "text-light" in content

def test_artplayer_autohide_defaults():
    """Verify that Artplayer uses default settings which include auto-hiding controls."""
    lightbox_path = Path("app/frontend/templates/partials/lightbox.html")
    content = lightbox_path.read_text()
    
    # Ensure isLive is not set to true (which might disable seeking/auto-hide in some configs)
    assert "isLive: true" not in content
    
    # Ensure we are using the standard player mode
    assert "new Artplayer" in content
