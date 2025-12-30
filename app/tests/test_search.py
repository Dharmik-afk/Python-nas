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
        mock_session.auth_header = "encrypted_dummy_header"
        mock_session.username = "testuser"
        mock_get.return_value = mock_session
        yield mock_get

@patch("app.backend.services.copyparty_service.proxy_api_request")
def test_search_files_success(mock_proxy, mock_authenticated_session):
    """Test successful file search."""
    mock_proxy.return_value = {
        "hits": [
            {"p": "folder1/file1.txt", "s": 1024, "t": 1600000000},
            {"p": "file2.jpg", "s": 2048, "t": 1600000001}
        ]
    }
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.get("/api/v1/fs/search?q=test")
        
        assert response.status_code == 200
        data = response.json()
        assert "hits" in data
        assert len(data["hits"]) == 2
        
        # Verify proxy was called with correct params
        # Copyparty search uses ?q=... and usually needs &json or similar
        # But our service might handle the path.
        # Typically search is at the root or a specific dir.
        mock_proxy.assert_called_once()
        args, kwargs = mock_proxy.call_args
        # args[1] should be the relative path, for global search it might be "." or ""
        assert kwargs["params"]["q"] == "test"

@patch("app.backend.services.copyparty_service.proxy_api_request")
def test_search_ui_success(mock_proxy, mock_authenticated_session):
    """Test successful search UI rendering."""
    mock_proxy.return_value = {
        "hits": [
            {"p": "folder1/file1.txt", "s": 1024, "t": 1600000000},
        ]
    }
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.get("/api/v1/fs/search/ui?q=test")
        
        assert response.status_code == 200
        assert "file1.txt" in response.text
        assert "folder1/file1.txt" in response.text

@patch("app.backend.routes.api_routes.validate_and_resolve_path")
def test_search_ui_empty_query(mock_resolve, mock_authenticated_session):
    """Test search UI returns directory listing when query is empty."""
    mock_path = MagicMock()
    mock_path.is_dir.return_value = True
    mock_path.iterdir.return_value = []
    mock_resolve.return_value = mock_path
    
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.get("/api/v1/fs/search/ui?q=&path=testdir")
        
        assert response.status_code == 200
        # Should render file_browser_content.html (empty state)
        assert "No items found" in response.text

def test_search_files_no_query(mock_authenticated_session):
    """Test search fails without query."""
    with TestClient(app) as client:
        client.cookies.set("session_id", "test_id")
        response = client.get("/api/v1/fs/search")
        assert response.status_code == 400
