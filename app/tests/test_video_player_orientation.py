import pytest
from pathlib import Path

def test_video_player_has_orientation_logic():
    """Verify that the video_player.js implements orientation and aspect ratio detection."""
    js_path = Path("app/frontend/static/js/video_player.js")
    content = js_path.read_text()
    
    assert "videoWidth" in content
    assert "videoHeight" in content
    assert "aspectRatio" in content
    assert "lockOrientation" in content or "screen.orientation" in content

def test_video_player_template_has_orientation_binding():
    """Verify that the video_player partial has orientation trigger bindings."""
    partial_path = Path("app/frontend/templates/partials/video_player.html")
    content = partial_path.read_text()
    
    assert "@loadedmetadata=\"initPlayer()\"" in content
    assert "toggleOrientation()" in content
