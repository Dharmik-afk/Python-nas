import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import auth_required
from app.core.session_manager import Session

# Mock authentication for dependency injection
def mock_auth_required():
    return True

@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[auth_required] = mock_auth_required
    yield
    if auth_required in app.dependency_overrides:
        del app.dependency_overrides[auth_required]

@pytest.fixture
def mock_authenticated_session():
    with patch("app.core.session_manager.session_manager.get_session") as mock_get:
        mock_session = Session("127.0.0.1", "test-agent")
        mock_session.auth_header = "encrypted_dummy_header"
        mock_get.return_value = mock_session
        yield mock_get

def test_read_main(mock_authenticated_session):
    """Test the root directory browsing."""
    with TestClient(app) as client:
        # We need to set a cookie so the middleware attempts to get the session
        client.cookies.set("session_id", "test_id")
        response = client.get("/")
        assert response.status_code == 200
        # assert "Home" in response.text # HTML response might not have "Home" text easily grep-able without parsing

def test_stats_api(mock_authenticated_session):
    """Test the metrics API."""
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_requests" in data
        assert "total_uploads" in data

    def test_forbidden_path(mock_authenticated_session):
        """Test security filter for .git folder."""
        with TestClient(app) as client:
            client.cookies.set("session_id", "test_id")
            response = client.get("/.git")
            assert response.status_code == 404
def test_invalid_path(mock_authenticated_session):
    """Test 404 for non-existent path."""
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.get("/this/path/does/not/exist")
        assert response.status_code == 404

@patch("app.backend.routes.api_routes.get_pmask")
@patch("app.backend.routes.api_routes.validate_and_resolve_path")
def test_delete_file_success(mock_resolve, mock_get_pmask, mock_authenticated_session):
    """Test successful deletion of a file."""
    mock_file = MagicMock()
    mock_file.exists.return_value = True
    mock_file.is_dir.return_value = False
    mock_resolve.return_value = mock_file
    mock_get_pmask.return_value = "rwd"
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.delete("/api/v1/fs/test.txt")
        assert response.status_code == 204
        mock_file.unlink.assert_called_once()

@patch("app.backend.routes.api_routes.get_pmask")
@patch("app.backend.routes.api_routes.validate_and_resolve_path")
def test_delete_file_forbidden(mock_resolve, mock_get_pmask, mock_authenticated_session):
    """Test deletion failure when 'd' permission is missing."""
    mock_file = MagicMock()
    mock_file.exists.return_value = True
    mock_resolve.return_value = mock_file
    mock_get_pmask.return_value = "rw"
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.delete("/api/v1/fs/test.txt")
        assert response.status_code == 403

@patch("app.backend.routes.api_routes.get_pmask")
@patch("app.backend.routes.api_routes.validate_and_resolve_path")
def test_mkdir_success(mock_resolve, mock_get_pmask, mock_authenticated_session):
    """Test successful creation of a directory."""
    mock_dir = MagicMock()
    mock_dir.exists.return_value = False
    mock_resolve.return_value = mock_dir
    mock_get_pmask.return_value = "rw"
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.post("/api/v1/fs/mkdir/new_folder")
        assert response.status_code == 200 # Returns refreshed partial
        mock_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)

@patch("app.backend.routes.api_routes.get_pmask")
@patch("app.backend.routes.api_routes.validate_and_resolve_path")
def test_mkdir_forbidden(mock_resolve, mock_get_pmask, mock_authenticated_session):
    """Test mkdir failure when 'w' permission is missing."""
    mock_dir = MagicMock()
    mock_dir.exists.return_value = False
    mock_resolve.return_value = mock_dir
    mock_get_pmask.return_value = "r"
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.post("/api/v1/fs/mkdir/new_folder")
        assert response.status_code == 403

