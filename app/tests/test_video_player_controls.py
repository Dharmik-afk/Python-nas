import pytest
from pathlib import Path

def test_video_player_partial_has_required_bindings():
    """Verify that the video_player partial has the required Alpine.js bindings for Phase 1."""
    partial_path = Path("app/frontend/templates/partials/video_player.html")
    content = partial_path.read_text()
    
    # Play/Pause
    assert "togglePlay()" in content
    assert "playing ? 'bi-pause-fill' : 'bi-play-fill'" in content
    
    # Seek/Scrub
    assert "startScrubbing($event)" in content
    assert "scrub($event)" in content
    assert "stopScrubbing()" in content
    assert "progressPercent" in content
    
    # Time display
    assert "formatTime(currentTime)" in content
    assert "formatTime(duration)" in content
    
    # Volume
    assert "toggleMute()" in content
    assert "updateVolume()" in content
    assert "x-model=\"volume\"" in content
    
    # Fullscreen
    assert "toggleFullscreen()" in content
    assert "isFullscreen ? 'bi-fullscreen-exit' : 'bi-fullscreen'" in content

def test_video_player_js_implements_required_methods():
    """Verify that the video_player.js implements the methods used in the template."""
    js_path = Path("app/frontend/static/js/video_player.js")
    content = js_path.read_text()
    
    required_methods = [
        "initPlayer",
        "togglePlay",
        "toggleMute",
        "updateVolume",
        "updateTime",
        "updateBuffer",
        "formatTime",
        "startScrubbing",
        "scrub",
        "stopScrubbing",
        "toggleFullscreen",
        "resetControlsTimer"
    ]
    
    for method in required_methods:
        assert f"{method}" in content
