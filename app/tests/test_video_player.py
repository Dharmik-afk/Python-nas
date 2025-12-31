import pytest
from pathlib import Path

def test_lightbox_has_custom_video_player():
    """Verify that the lightbox template contains the custom video player UI."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    assert "video-player-container" in content
    assert "x-ref=\"video\"" in content
    assert "togglePlay()" in content
    assert "bi-play-fill" in content
    assert "bi-pause-fill" in content
    assert "showControls" in content

