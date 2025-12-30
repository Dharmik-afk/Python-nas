import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.backend.database.models import User
from app.core.security import hasher

@pytest.fixture
def mock_db_user():
    user = User(
        username="testuser",
        hashed_password=hasher.get_password_hash("testpass"),
        is_active=True,
        permissions="r"
    )
    return user

@patch("app.backend.routes.auth_routes.SessionLocal")
@patch("app.backend.routes.auth_routes.get_user_permissions_from_config")
@patch("app.backend.routes.auth_routes.verify_with_copyparty")
def test_login_fetches_permissions(mock_verify, mock_get_perms, mock_session_local, mock_db_user):
    # Setup mock DB
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    mock_db.query.return_value.filter.return_value.first.return_value = mock_db_user
    
    # Setup mocks
    mock_verify.return_value = True
    mock_get_perms.return_value = "rwma"
    
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "testuser", "password": "testpass"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["permissions"] == "rwma"
        
        # Verify that the session has the correct permissions
        # We need to find the session in the session_manager
        from app.core.session_manager import session_manager
        # Get session_id from cookie
        session_id = client.cookies.get("session_id")
        session = session_manager.get_session(session_id)
        assert session is not None
        assert session.permissions == "rwma"

@patch("app.backend.routes.auth_routes.SessionLocal")
@patch("app.backend.routes.auth_routes.get_user_permissions_from_config")
@patch("app.backend.routes.auth_routes.verify_with_copyparty")
def test_token_fetches_permissions(mock_verify, mock_get_perms, mock_session_local, mock_db_user):
    # Setup mock DB
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    mock_db.query.return_value.filter.return_value.first.return_value = mock_db_user
    
    # Setup mocks
    mock_verify.return_value = True
    mock_get_perms.return_value = "r"
    
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/token",
            data={"username": "testuser", "password": "testpass"}
        )
        
        assert response.status_code == 200
        # Token schema doesn't have permissions yet, but JWT should have it
        data = response.json()
        assert "access_token" in data
        
        # Decode JWT and check permissions
        from jose import jwt
        from app.core.config import settings
        payload = jwt.decode(data["access_token"], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["permissions"] == "r"