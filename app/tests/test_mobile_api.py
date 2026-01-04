import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock
from pathlib import Path
from app.backend.database.session import SessionLocal
from app.backend.database.models import User
from app.core.security import hasher

client = TestClient(app)

@pytest.fixture
def auth_header(mock_db_user):
    user, password = mock_db_user
    with patch("app.backend.routes.auth_routes.verify_with_copyparty", return_value=True), \
         patch("app.backend.routes.auth_routes.get_user_permissions_from_config", return_value={"r": ["/"], "w": ["/"]}), \
         patch("app.backend.routes.auth_routes.sync_users_to_copyparty"):
         
        response = client.post(
            "/api/v1/auth/token",
            data={"username": user.username, "password": password}
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def mock_db_user():
    db = SessionLocal()
    username = "testmobileapi"
    password = "testpassword"
    hashed_password = hasher.get_password_hash(password)
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(username=username, hashed_password=hashed_password, is_active=True, permissions="r")
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.hashed_password = hashed_password
        db.commit()
        
    yield user, password
    
    db.delete(user)
    db.commit()
    db.close()

def test_list_directory_json(auth_header):
    """TDD: Test for the new JSON directory listing endpoint."""
    with patch("app.backend.routes.api_routes.validate_and_resolve_path") as mock_resolve, \
         patch("app.backend.routes.api_routes.get_pmask", return_value="rw"), \
         patch("app.backend.routes.api_routes.is_path_forbidden", return_value=False):
        
        # Mock directory contents
        mock_file = MagicMock()
        mock_file.name = "testfile.txt"
        mock_file.is_dir.return_value = False
        mock_file.stat.return_value.st_size = 1024
        mock_file.stat.return_value.st_mtime = 1672531200 # 2023-01-01
        
        mock_dir = MagicMock()
        mock_dir.name = "testfolder"
        mock_dir.is_dir.return_value = True
        mock_dir.stat.return_value.st_size = 4096
        mock_dir.stat.return_value.st_mtime = 1672531200
        
        mock_resolved_path = MagicMock()
        mock_resolved_path.is_dir.return_value = True
        mock_resolved_path.iterdir.return_value = [mock_file, mock_dir]
        mock_resolve.return_value = mock_resolved_path
        
        response = client.get("/api/v1/fs/list/", headers=auth_header)
        
        # This is expected to FAIL initially because the endpoint doesn't exist
        assert response.status_code == 200
        data = response.json()
        assert "path" in data
        assert "items" in data
        assert len(data["items"]) == 2
        
        # Verify item structure
        first_item = data["items"][0]
        assert "name" in first_item
        assert "is_dir" in first_item
        assert "size" in first_item
        assert "mtime" in first_item
        assert "permissions" in first_item

def test_search_json(auth_header):
    """TDD: Test for the JSON search results endpoint."""
    mock_search_results = {
        "hits": [
            {"p": "folder/file1.txt", "s": 1024, "t": 1672531200},
            {"p": "folder/subfolder/", "s": 4096, "t": 1672531200}
        ]
    }
    
    with patch("app.backend.routes.api_routes.search_files", return_value=mock_search_results), \
         patch("app.backend.routes.api_routes.get_pmask", return_value="r"):
        
        # Test with format=json query parameter
        response = client.get("/api/v1/fs/search?q=test&format=json", headers=auth_header)
        
        # This is expected to return the raw copyparty JSON currently, but we want it transformed
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 2
        
        # Verify transformed structure
        first_item = data["items"][0]
        assert first_item["name"] == "file1.txt"
        assert first_item["is_dir"] is False
        assert first_item["permissions"] == "r"

def test_gallery_metadata_json(auth_header):
    """TDD: Test for the gallery metadata JSON endpoint."""
    with patch("app.backend.routes.api_routes.validate_and_resolve_path") as mock_resolve, \
         patch("app.backend.routes.api_routes.get_pmask", return_value="r"):
        
        # Mock media file
        mock_file = MagicMock()
        mock_file.name = "image.jpg"
        mock_file.is_file.return_value = True
        mock_file.suffix = ".jpg"
        
        mock_resolved_dir = MagicMock()
        mock_resolved_dir.is_dir.return_value = True
        mock_resolved_dir.iterdir.return_value = [mock_file]
        mock_resolve.return_value = mock_resolved_dir
        
        response = client.get("/api/v1/gallery/folder", headers=auth_header)
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 1
        
        item = data["items"][0]
        assert "name" in item
        assert "url" in item
        assert "thumb" in item
        assert "type" in item
        assert item["type"] == "image"
        # Verify thumb URL contains parameter
        assert "?thumb=" in item["thumb"]

def test_thumbnail_proxy_auth(auth_header):
    """TDD: Test that thumbnail requests are protected and accept Bearer tokens."""
    with patch("app.backend.routes.download_routes.validate_and_resolve_path") as mock_resolve, \
         patch("app.backend.routes.download_routes.copyparty_service.proxy_stream_request") as mock_proxy:
        
        mock_file = MagicMock()
        mock_file.is_file.return_value = True
        mock_file.relative_to.return_value = Path("test.jpg")
        mock_resolve.return_value = mock_file
        
        # Simulating a successful proxy response
        mock_proxy.return_value = {"status": "streaming"}
        
        response = client.get("/download/test.jpg?thumb=300x300", headers=auth_header)
        
        assert response.status_code == 200
        assert mock_proxy.called
        
        # Verify it fails without token
        client.cookies.clear()
        response = client.get("/download/test.jpg?thumb=300x300")
        assert response.status_code == 401
