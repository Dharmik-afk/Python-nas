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


def test_artplayer_has_ui_controls_configuration():
    """Verify that Artplayer initialization includes required UI controls."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    assert "fullscreen: true" in content
    assert "setting: true" in content
    assert "playbackRate: true" in content
    
def test_thumbnail_mode_logic():
    """Verify that thumbnail mode logic is present."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    assert "videoMode === 'thumbnail'" in content
    assert "videoMode === 'player'" in content
    assert "startVideo()" in content
    assert "bi-play-fill" in content # Play button



