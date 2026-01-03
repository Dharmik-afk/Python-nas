import pytest
from app.core.security import hasher

def test_duplicate_password_hashing_collision():
    """
    Reproduce the issue where identical passwords produce identical Copyparty hashes
    due to a static salt, causing conflicts in the backend.
    """
    password = "MySecurePassword123!"
    
    # Generate hash for User A
    internal_a = hasher.get_internal_proxy_password(password, "userA")
    hash_a = hasher.get_copyparty_hash(internal_a)
    
    # Generate hash for User B
    internal_b = hasher.get_internal_proxy_password(password, "userB")
    hash_b = hasher.get_copyparty_hash(internal_b)
    
    # After fix: They should be DIFFERENT because they are salted by username.
    assert hash_a != hash_b, "Hashes for the same password should be unique (salted by username)"
    
    # Also verify that it's deterministic for the same user
    assert hash_a == hasher.get_copyparty_hash(internal_a)
