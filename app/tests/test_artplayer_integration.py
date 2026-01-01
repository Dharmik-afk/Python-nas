import pytest
from pathlib import Path

def test_lightbox_has_artplayer_container():
    """Verify that the lightbox template contains the Artplayer container."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    # This test is expected to FAIL initially until we update the template
    content = template_path.read_text()
    
    assert 'id="artplayer-app"' in content or 'class="artplayer-app"' in content
    assert "artplayer.js" in content
    assert "artplayer.css" in content

def test_artplayer_initialization_logic():
    """Verify that the initialization logic for Artplayer is present in the frontend scripts."""
    # Assuming initialization will be in a new or updated JS file
    # This is a placeholder for checking the script content
    pass
