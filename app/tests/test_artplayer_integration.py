import pytest
from pathlib import Path

def test_artplayer_assets_in_base_layout():
    """Verify that Artplayer assets are included in the base layout."""
    base_path = Path("app/frontend/templates/layouts/base.html")
    content = base_path.read_text()
    assert "artplayer.js" in content
    assert "artplayer.css" in content

def test_lightbox_has_artplayer_container():
    """Verify that the lightbox template contains the Artplayer container."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    assert 'id="artplayer-app"' in content or 'class="artplayer-app"' in content


def test_artplayer_initialization_logic():
    """Verify that the initialization logic for Artplayer is present in the frontend scripts."""
    # Assuming initialization will be in a new or updated JS file
    # This is a placeholder for checking the script content
    pass
