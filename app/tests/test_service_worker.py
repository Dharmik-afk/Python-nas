import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import auth_required
from app.core.session_manager import Session

# Mock authentication for dependency injection
def mock_auth_required():
    return True

app.dependency_overrides[auth_required] = mock_auth_required

@pytest.fixture
def mock_authenticated_session():
    with patch("app.core.session_manager.session_manager.get_session") as mock_get:
        mock_session = Session("127.0.0.1", "test-agent")
        mock_session.auth_header = "encrypted_dummy_header"
        mock_get.return_value = mock_session
        yield mock_get

def test_service_worker_served(mock_authenticated_session):
    """Test that sw.js is served at the root with correct MIME type."""
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.get("/sw.js")
        assert response.status_code == 200
        assert "application/javascript" in response.headers["content-type"]

def test_service_worker_registered_in_base_html(mock_authenticated_session):
    """Test that base.html contains the SW registration script."""
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.get("/")
        assert response.status_code == 200
        assert "navigator.serviceWorker.register" in response.text
        assert "/sw.js" in response.text
