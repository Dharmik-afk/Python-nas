import pytest
from pathlib import Path

def test_video_player_refinements():
    """Verify video player refinements: seeking, inverted gestures, and UI visibility logic."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    # Seeking logic
    assert "seekVideo" in content
    assert "input type=\"range\"" in content
    assert "formatTime" in content
    
    # UI Visibility Logic
    assert "x-show=\"currentItem?.type !== 'video' || !playing\"" in content
    
    # Corrected Gestures (Inverted Y)
    # Swipe UP (negative deltaY in logic, but positive effect) -> Volume UP
    # My implementation: deltaY = startY - endY (so Up is positive)
    # change = deltaY / height (so Up increases value)
    assert "deltaY = this.touchStartY - e.touches[0].clientY" in content
    assert "this.initialVolume + change" in content
