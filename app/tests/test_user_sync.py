import pytest
from unittest.mock import MagicMock, patch, mock_open
from app.core.user_sync import sync_users_to_copyparty
from app.backend.database.models import User

@patch("scripts.manage.SessionLocal")
@patch("builtins.open", new_callable=mock_open)
@patch("scripts.manage.settings")
def test_sync_users_to_copyparty(mock_settings, mock_file, mock_session_local):
    # Setup mock settings
    mock_settings.BASE_DIR = MagicMock()
    # Mocking path construction: settings.BASE_DIR / "copyparty" / "copyparty.conf"
    mock_path_copyparty = MagicMock()
    mock_path_conf = MagicMock()
    
    # Chain of Truedivs
    mock_settings.BASE_DIR.__truediv__.side_effect = lambda x: mock_path_copyparty if x == "copyparty" else MagicMock()
    mock_path_copyparty.__truediv__.return_value = mock_path_conf
    
    # Mock SERVE_PATH
    mock_serve_path = MagicMock()
    mock_settings.SERVE_PATH.resolve.return_value = mock_serve_path
    mock_serve_path.__str__.return_value = "/mock/serve/path"

    # Setup mock DB session
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    
    # Mock users
    user1 = User(username="admin", cp_hash="hash1", permissions="admin", is_active=True)
    user2 = User(username="user", cp_hash="hash2", permissions="r", is_active=True)
    mock_db.query.return_value.filter.return_value.all.return_value = [user1, user2]

    # Call function
    sync_users_to_copyparty()

    # Verify file write
    handle = mock_file()
    handle.write.assert_called_once()
    content = handle.write.call_args[0][0]
    
    assert "-a admin:hash1" in content
    assert "-a user:hash2" in content
    # Order of permissions might vary, so check presence of parts
    assert "/mock/serve/path:/" in content
    assert "rwmda.,admin" in content
    assert "r,user" in content
