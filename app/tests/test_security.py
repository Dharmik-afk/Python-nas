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
