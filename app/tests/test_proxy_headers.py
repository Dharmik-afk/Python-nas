import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import auth_required
from pathlib import Path

# Mock authentication
def mock_auth_required():
    return True

app.dependency_overrides[auth_required] = mock_auth_required

@pytest.fixture
def mock_session():
    with patch("app.core.session_manager.session_manager.get_session") as mock_get:
        session = MagicMock()
        session.username = "testuser"
        session.auth_header = "encrypted_header"
        mock_get.return_value = session
        yield session

@patch("app.backend.services.copyparty_service.decrypt_string")
@patch("app.backend.services.copyparty_service.requests.get")
@patch("app.backend.routes.download_routes.validate_and_resolve_path")
def test_download_proxies_auth_header(mock_resolve, mock_get, mock_decrypt, mock_session):
    """Verify that the Authorization header is propagated to copyparty during download."""
    # Setup mocks
    mock_path = MagicMock()
    mock_path.is_file.return_value = True
    mock_path.name = "test.txt"
    mock_path.relative_to.return_value = Path("test.txt")
    mock_resolve.return_value = mock_path
    
    mock_decrypt.return_value = "Basic dGVzdHVzZXI6cGFzcw==" # Decrypted "testuser:pass"
    
    # Mock requests.get response
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.headers = {"Content-Type": "text/plain"}
    mock_resp.iter_content.return_value = iter([b"content"])
    mock_get.return_value = mock_resp
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.get("/download/test.txt")
        
        assert response.status_code == 200
        
        # Verify requests.get was called with the correct Authorization header
        args, kwargs = mock_get.call_args
        headers = kwargs.get("headers", {})
        assert headers.get("Authorization") == "Basic dGVzdHVzZXI6cGFzcw=="
