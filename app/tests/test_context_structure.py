import os
import pytest

def test_context_directory_exists():
    """Verify that the root .context directory exists."""
    assert os.path.isdir(".context"), "The root .context/ directory should exist."

def test_security_overlay_exists():
    """Verify that the security overlay exists."""
    assert os.path.isfile(".context/security.md"), "The .context/security.md overlay should exist."

def test_gemini_protocol_exists():
    """Verify that GEMINI.md contains the Context Loading Protocol."""
    assert os.path.isfile("GEMINI.md"), "GEMINI.md should exist."
    with open("GEMINI.md", "r") as f:
        content = f.read()
    assert "Context Loading Protocol" in content, "GEMINI.md should contain 'Context Loading Protocol'."
