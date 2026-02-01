import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import auth_required
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
def mock_session():
    with patch("app.core.session_manager.session_manager.get_session") as mock_get:
        session = MagicMock()
        session.username = "testuser"
        session.permissions = "rw"
        session.auth_header = "encrypted_header"
        mock_get.return_value = session
        yield session

@patch("app.frontend.routes.frontend_routes.get_pmask")
@patch("app.frontend.routes.frontend_routes.validate_and_resolve_path")
def test_ui_upload_button_visibility(mock_resolve, mock_pmask, mock_session):
    """Verify that Upload button visibility depends on 'w' permission."""
    # Setup mock path
    mock_path = MagicMock()
    mock_path.is_dir.return_value = True
    mock_path.iterdir.return_value = []
    mock_resolve.return_value = mock_path
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        
        # Case 1: Has 'w' permission
        mock_pmask.return_value = "rw"
        response = client.get("/")
        assert response.status_code == 200
        assert "UPLOAD FILES" in response.text
        
        # Case 2: No 'w' permission
        mock_pmask.return_value = "r"
        response = client.get("/")
        assert response.status_code == 200
        assert "UPLOAD FILES" not in response.text

@patch("app.frontend.routes.frontend_routes.get_pmask")
@patch("app.frontend.routes.frontend_routes.validate_and_resolve_path")
def test_ui_delete_button_visibility(mock_resolve, mock_pmask, mock_session):
    """Verify that Delete button visibility depends on 'd' permission."""
    # Setup mock path with one file
    mock_file = MagicMock()
    mock_file.name = "test.txt"
    mock_file.is_dir.return_value = False
    mock_file.is_file.return_value = True
    mock_file.suffix = ".txt"
    
    mock_dir = MagicMock()
    mock_dir.is_dir.return_value = True
    mock_dir.iterdir.return_value = [mock_file]
    mock_resolve.return_value = mock_dir
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        
        # Case 1: Has 'd' permission
        mock_pmask.return_value = "rwd"
        response = client.get("/")
        assert response.status_code == 200
        assert "bi-trash-fill" in response.text
        
        # Case 2: No 'd' permission
        mock_pmask.return_value = "rw"
        response = client.get("/")
        assert response.status_code == 200
        assert "bi-trash-fill" not in response.text

@patch("app.frontend.routes.frontend_routes.get_pmask")
@patch("app.frontend.routes.frontend_routes.validate_and_resolve_path")
def test_ui_create_folder_button_visibility(mock_resolve, mock_pmask, mock_session):
    """Verify that Create Folder button visibility depends on 'w' permission."""
    # Setup mock path
    mock_path = MagicMock()
    mock_path.is_dir.return_value = True
    mock_path.iterdir.return_value = []
    mock_resolve.return_value = mock_path
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        
        # Case 1: Has 'w' permission
        mock_pmask.return_value = "rw"
        response = client.get("/")
        assert response.status_code == 200
        assert "CREATE FOLDER" in response.text
        
        # Case 2: No 'w' permission
        mock_pmask.return_value = "r"
        response = client.get("/")
        assert response.status_code == 200
        assert "CREATE FOLDER" not in response.text
