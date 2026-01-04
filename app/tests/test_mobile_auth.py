import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.core.security import hasher
from app.backend.database.session import SessionLocal
from app.backend.database.models import User
from unittest.mock import patch, MagicMock

client = TestClient(app)

@pytest.fixture
def mock_db_user():
    # Create a dummy user in the DB for testing
    db = SessionLocal()
    username = "testmobileuser"
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
    
    # Cleanup
    db.delete(user)
    db.commit()
    db.close()

def test_token_endpoint(mock_db_user):
    user, password = mock_db_user
    
    # Mock the Copyparty verification and permission check
    with patch("app.backend.routes.auth_routes.verify_with_copyparty", return_value=True), \
         patch("app.backend.routes.auth_routes.get_user_permissions_from_config", return_value={"r": ["/"], "w": ["/"]}), \
         patch("app.backend.routes.auth_routes.sync_users_to_copyparty"):
         
        response = client.post(
            "/api/v1/auth/token",
            data={"username": user.username, "password": password}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        
        token = data["access_token"]
        
        # Verify access using ONLY the header (clear cookies)
        client.cookies.clear()
        
        # Mock filesystem calls for the gallery endpoint
        with patch("app.backend.routes.api_routes.validate_and_resolve_path") as mock_resolve, \
             patch("app.backend.routes.api_routes.get_pmask", return_value="r"):
            
            # Setup mock directory structure
            mock_path = MagicMock()
            mock_path.is_dir.return_value = True
            mock_path.is_file.return_value = False
            mock_path.iterdir.return_value = [] # Return empty list of files
            mock_resolve.return_value = mock_path
            
            headers = {"Authorization": f"Bearer {token}"}
            # Use /gallery/ which expects a path. We use 'root' which maps to base serve dir usually.
            response = client.get("/api/v1/gallery/root", headers=headers)
            
            # Note: The gallery endpoint attempts to resolve 'root'.
            # If our mock_resolve works, it should return 200.
            # However, validate_and_resolve_path might raise 404 if 'root' doesn't exist relative to SERVE_DIR.
            # But we mocked validate_and_resolve_path to return a valid mock_path object.
            
            assert response.status_code == 200
            assert "items" in response.json()

def test_bearer_token_authentication(mock_db_user):
    user, password = mock_db_user
    
    with patch("app.backend.routes.auth_routes.verify_with_copyparty", return_value=True), \
         patch("app.backend.routes.auth_routes.get_user_permissions_from_config", return_value={"r": ["/"], "w": ["/"],}), \
         patch("app.backend.routes.auth_routes.sync_users_to_copyparty"):
        
        # 1. Get Token
        response = client.post(
            "/api/v1/auth/token",
            data={"username": user.username, "password": password}
        )
        token = response.json()["access_token"]
        
        # 2. Test Access to a protected route (We will verify api_routes.py first to find one)
        pass