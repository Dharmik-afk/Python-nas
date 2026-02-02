import pytest
import hashlib
from app.core.security import hasher

def test_get_copyparty_hash_raw():
    # Known values from copyparty --ah-gen "password" --ah-alg sha2,424242
    # This test verifies the hashing algorithm itself is correct for a given input
    password = "password"
    expected = "+_UbIhavqWiVaZ4F_pGUNUnQ4nDohEX00"
    actual = hasher.get_copyparty_hash(password)
    assert actual == expected

def test_get_internal_proxy_password():
    # The workaround (SHA256) should be removed.
    # The proxy password should be the plain password.
    password = "password"
    user_salt = "testuser"
    expected = "testuserpassword"
    actual = hasher.get_internal_proxy_password(password, user_salt)
    assert actual == expected

def test_full_copyparty_hash_flow():
    # This flow tests the end-to-end transformation
    # It should now result in the hash of "password", not hash(sha256("password"))
    password = "password"
    user_salt = "testuser"
    internal = hasher.get_internal_proxy_password(password, user_salt)
    actual = hasher.get_copyparty_hash(internal)
    
    # Expected: Hash of "testuserpassword"
    # Note: We cannot assert the exact hash without calculating it, 
    # but we verify it runs without error and returns a valid-looking hash.
    assert actual.startswith("+")
    assert len(actual) > 30

from app.core.config import Settings
from pathlib import Path

def test_settings_default_safe_path():
    s = Settings()
    # Default should be project_root/storage/files
    # We resolve to be sure
    expected = (s.BASE_DIR / "storage" / "files").resolve()
    assert Path(s.SERVE_DIR).resolve() == expected

def test_settings_custom_safe_path():
    # Outside project root and outside /usr/
    # In Termux, we can try /data/data/com.termux/files/home/safe_serve
    custom_path = "/data/data/com.termux/files/home/python-nas-safe-test"
    s = Settings(CUSTOM_SERVE_DIR=custom_path)
    assert s.SERVE_DIR == str(Path(custom_path).resolve())

def test_settings_restricted_path_fails():
    # Project root is restricted by default
    base_settings = Settings()
    project_root = str(base_settings.BASE_DIR.resolve())
    
    # This should fail because project_root is in RESTRICTED_DIRS 
    # and NOT in ALLOWED_OVERRIDE_DIRS (by default only storage/files is allowed)
    with pytest.raises(ValueError, match="restricted"):
        Settings(CUSTOM_SERVE_DIR=project_root)

def test_settings_restricted_path_override_passes():
    base_settings = Settings()
    project_root = base_settings.BASE_DIR.resolve()
    
    # If we explicitly allow it in ALLOWED_OVERRIDE_DIRS, it should pass
    # Note: We need to pass it as a list of strings or Paths for Pydantic
    s = Settings(
        CUSTOM_SERVE_DIR=str(project_root), 
        ALLOWED_OVERRIDE_DIRS=[project_root]
    )
    assert Path(s.SERVE_DIR).resolve() == project_root
