import os
import pytest

def test_context_directory_exists():
    """Verify that the root .context directory exists."""
    assert os.path.isdir(".context"), "The root .context/ directory should exist."
