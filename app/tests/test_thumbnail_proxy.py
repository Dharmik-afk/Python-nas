import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi.responses import Response
from app.main import app
from app.core.auth import auth_required
from app.core.session_manager import Session

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
        mock_get.return_value = mock_session
        yield mock_get

@patch("app.backend.routes.download_routes.validate_and_resolve_path")
@patch("app.backend.services.copyparty_service.proxy_stream_request", new_callable=AsyncMock)
def test_thumbnail_param_forwarding(mock_proxy, mock_resolve, mock_authenticated_session):
    """
    Test that the download route correctly forwards the 'thumb' query parameter
    to the copyparty service.
    """
    # Mock file system check
    mock_file = MagicMock()
    mock_file.is_file.return_value = True
    # Mock relative_to to return a clean string path
    mock_file.relative_to.return_value = "video.mp4"
    mock_resolve.return_value = mock_file

    # Configure the mock proxy to return a simple Response object
    mock_proxy.return_value = Response(content=b"fake-image-data", media_type="image/jpeg")

    with TestClient(app) as client:
        # Set session cookie
        client.cookies.set("session_id", "test_id")
        
        # Request with thumb parameter
        response = client.get("/download/video.mp4?thumb=400")
        
        # Verify response
        assert response.status_code == 200
        assert response.content == b"fake-image-data"
        
        # Verify proxy was called with correct params
        mock_proxy.assert_called_once()
        call_args = mock_proxy.call_args
        # Check named arguments
        assert "params" in call_args.kwargs
        assert call_args.kwargs["params"] == {"thumb": "400"}
