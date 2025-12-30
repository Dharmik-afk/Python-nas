import pytest
import json
import time
from pathlib import Path
from app.core.session_manager import Session, SessionManager

def test_session_persistence(tmp_path):
    save_path = tmp_path / "sessions.json"
    manager = SessionManager(save_path=save_path)
    
    # Create a session
    session = manager.create_session("127.0.0.1", "test-agent")
    session.username = "testuser"
    session.auth_header = "encrypted_auth"
    session.permissions = "rw"
    sid = session.session_id
    
    # Save sessions
    manager.save_sessions()
    assert save_path.exists()
    
    # Create a new manager instance and load sessions
    new_manager = SessionManager(save_path=save_path)
    restored_session = new_manager.get_session(sid)
    
    assert restored_session is not None
    assert restored_session.username == "testuser"
    assert restored_session.auth_header == "encrypted_auth"
    assert restored_session.permissions == "rw"
    assert restored_session.session_id == sid

def test_session_expiry(tmp_path):
    save_path = tmp_path / "sessions.json"
    # Create manager with 1 second timeout
    with patch("app.core.config.settings.SESSION_TIMEOUT_SECONDS", 1):
        manager = SessionManager(save_path=save_path)
        session = manager.create_session("127.0.0.1", "test-agent")
        sid = session.session_id
        
        # Wait for expiry
        time.sleep(1.1)
        
        assert manager.get_session(sid) is None
        manager.cleanup_expired_sessions()
        
        # Reload and check
        new_manager = SessionManager(save_path=save_path)
        assert new_manager.get_session(sid) is None

from unittest.mock import patch
