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


def test_artplayer_has_custom_gesture_configuration():
    """Verify that Artplayer initialization includes custom gesture logic placeholders."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    # We expect these to be added in Phase 3
    assert "layers:" in content or "custom" in content.lower()
    assert "backward" in content.lower() or "forward" in content.lower()

