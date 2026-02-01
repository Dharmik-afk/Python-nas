import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import auth_required
from app.core.session_manager import Session
from pathlib import Path

# Mock authentication
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
        mock_session.username = "testuser"
        mock_get.return_value = mock_session
        yield mock_get

@patch("app.backend.routes.api_routes.validate_and_resolve_path")
@patch("app.backend.routes.api_routes.get_pmask")
@patch("app.backend.routes.api_routes.rename_item")
def test_rename_file_success(mock_rename, mock_get_pmask, mock_resolve, mock_authenticated_session):
    """Test successful file renaming."""
    mock_file = MagicMock()
    mock_file.exists.return_value = True
    mock_resolve.return_value = mock_file
    mock_get_pmask.return_value = "rwdm" # 'm' is move/rename in copyparty
    mock_rename.return_value = True
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.post("/api/v1/fs/rename/old.txt?new_name=new.txt")
        
        assert response.status_code == 200
        mock_rename.assert_called_once()
        args, kwargs = mock_rename.call_args
        # args[1] is Path("old.txt")
        assert args[1] == Path("old.txt")
        assert args[2] == "new.txt"

@patch("app.backend.routes.api_routes.validate_and_resolve_path")
@patch("app.backend.routes.api_routes.get_pmask")
def test_rename_file_forbidden(mock_get_pmask, mock_resolve, mock_authenticated_session):
    """Test rename failure when 'm' permission is missing."""
    mock_file = MagicMock()
    mock_file.exists.return_value = True
    mock_resolve.return_value = mock_file
    mock_get_pmask.return_value = "rw" # Missing 'm'
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.post("/api/v1/fs/rename/old.txt?new_name=new.txt")
        assert response.status_code == 403

    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.post("/api/v1/fs/rename/old.txt?new_name=new.txt")
        assert response.status_code == 403

def test_rename_file_no_new_name(mock_authenticated_session):
    """Test rename fails without new_name."""
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.post("/api/v1/fs/rename/old.txt")
        assert response.status_code == 400
