import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import auth_required
from app.core.session_manager import Session

# Mock authentication
def mock_auth_required():
    return True

app.dependency_overrides[auth_required] = mock_auth_required

@pytest.fixture
def mock_authenticated_session():
    with patch("app.core.session_manager.session_manager.get_session") as mock_get:
        mock_session = Session("127.0.0.1", "test-agent")
        mock_get.return_value = mock_session
        yield mock_get

@patch("app.backend.routes.api_routes.get_pmask")
@patch("app.backend.routes.api_routes.validate_and_resolve_path")
def test_delete_notification_header(mock_resolve, mock_get_pmask, mock_authenticated_session):
    """Verify HX-Trigger header on delete."""
    mock_file = MagicMock()
    mock_file.exists.return_value = True
    mock_file.is_dir.return_value = False
    mock_resolve.return_value = mock_file
    mock_get_pmask.return_value = "rwd"
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.delete("/api/v1/fs/test.txt")
        assert response.status_code == 204
        assert "HX-Trigger" in response.headers
        assert "show-toast" in response.headers["HX-Trigger"]
        assert "deleted successfully" in response.headers["HX-Trigger"]

@patch("app.backend.routes.api_routes.get_pmask")
@patch("app.backend.routes.api_routes.validate_and_resolve_path")
def test_mkdir_notification_header(mock_resolve, mock_get_pmask, mock_authenticated_session):
    """Verify HX-Trigger header on mkdir."""
    mock_dir = MagicMock()
    mock_dir.exists.return_value = False
    mock_resolve.return_value = mock_dir
    mock_get_pmask.return_value = "rw"
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.post("/api/v1/fs/mkdir/new_folder")
        assert response.status_code == 200
        assert "HX-Trigger" in response.headers
        assert "Folder created successfully" in response.headers["HX-Trigger"]

@patch("app.backend.routes.api_routes.validate_and_resolve_path")
@patch("app.backend.routes.api_routes.get_pmask")
@patch("app.backend.routes.api_routes.rename_item")
def test_rename_notification_header(mock_rename, mock_get_pmask, mock_resolve, mock_authenticated_session):
    """Verify HX-Trigger header on rename."""
    mock_file = MagicMock()
    mock_file.exists.return_value = True
    mock_resolve.return_value = mock_file
    mock_get_pmask.return_value = "rwdm"
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.post("/api/v1/fs/rename/old.txt?new_name=new.txt")
        assert response.status_code == 200
        assert "HX-Trigger" in response.headers
        assert "Item renamed successfully" in response.headers["HX-Trigger"]
