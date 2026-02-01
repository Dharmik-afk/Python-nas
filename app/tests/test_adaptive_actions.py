import pytest
from pathlib import Path

def test_lightbox_adaptive_actions():
    """Verify that the lightbox template contains permission-aware action buttons."""
    template_path = Path("app/frontend/templates/partials/lightbox.html")
    content = template_path.read_text()
    
    # State
    assert 'pmask: ""' in content
    assert "this.pmask = data.pmask" in content
    
    # Permission Checks
    assert "template x-if=\"pmask.includes('m')\"" in content # Rename
    assert "template x-if=\"pmask.includes('d')\"" in content # Delete
    
    # Handlers
    assert "handleRename()" in content
    assert "handleDelete()" in content
    assert "fetch(" in content
    assert "`/api/v1/fs/rename/" in content
    assert 'method: "DELETE"' in content
