import os
import pytest

def test_context_directory_exists():
    """Verify that the root .context directory exists."""
    assert os.path.isdir(".context"), "The root .context/ directory should exist."

def test_security_overlay_exists():
    """Verify that the security overlay exists."""
    assert os.path.isfile(".context/security.md"), "The .context/security.md overlay should exist."
