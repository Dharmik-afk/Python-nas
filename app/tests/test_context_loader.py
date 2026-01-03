import os
import subprocess
import pytest

# Define the path to the loader script
LOADER_SCRIPT = "scripts/context_loader.py"

@pytest.fixture
def mock_context_tree(tmp_path):
    """Create a temporary directory structure with context files for testing."""
    # Root level
    root_gemini = tmp_path / "GEMINI.md"
    root_gemini.write_text("# Root GEMINI\nGlobal context")
    
    context_dir = tmp_path / ".context"
    context_dir.mkdir()
    security_overlay = context_dir / "security.md"
    security_overlay.write_text("# Security Overlay\nSecurity rules")
    
    # Subdir level
    app_dir = tmp_path / "app"
    app_dir.mkdir()
    app_context = app_dir / ".context.md"
    app_context.write_text("# App Context\nApp specific rules")
    
    # Deep level
    backend_dir = app_dir / "backend"
    backend_dir.mkdir()
    backend_context = backend_dir / ".context.md"
    backend_context.write_text("# Backend Context\nBackend specific rules")
    
    return tmp_path

def run_loader(args):
    """Helper to run the loader script with arguments."""
    result = subprocess.run(
        ["python", LOADER_SCRIPT] + args,
        capture_output=True,
        text=True
    )
    return result

def test_loader_exists():
    """Verify the loader script exists."""
    assert os.path.isfile(LOADER_SCRIPT)

def test_loader_merges_upward(mock_context_tree):
    """Verify that the loader merges context from deep path upwards."""
    backend_path = mock_context_tree / "app" / "backend"
    result = run_loader(["--path", str(backend_path)])
    
    assert result.returncode == 0
    # Check for resolution order (Nearest First)
    # The output should contain Backend, then App, then Root
    output = result.stdout
    assert "Backend Context" in output
    assert "App Context" in output
    assert "Root GEMINI" in output
    
    # Basic check for attribution
    assert str(backend_path / ".context.md") in output

def test_loader_task_overlay(mock_context_tree):
    """Verify that --task loads the corresponding overlay."""
    result = run_loader(["--path", str(mock_context_tree), "--task", "security"])
    
    assert result.returncode == 0
    assert "Security Overlay" in result.stdout
    assert "Security rules" in result.stdout

def test_loader_invalid_path():
    """Verify error handling for invalid path."""
    result = run_loader(["--path", "/non/existent/path"])
    assert result.returncode != 0
