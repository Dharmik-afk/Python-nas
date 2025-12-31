import pytest
from app.core.security import hasher

def test_duplicate_password_hashing_collision():
    """
    Reproduce the issue where identical passwords produce identical Copyparty hashes
    due to a static salt, causing conflicts in the backend.
    """
    password = "MySecurePassword123!"
    
    # Generate hash for User A
    hash_a = hasher.get_copyparty_hash(password)
    
    # Generate hash for User B
    hash_b = hasher.get_copyparty_hash(password)
    
    # CURRENT BEHAVIOR: They are identical because the salt is hardcoded.
    # We want to change this behavior so that they are unique.
    # Therefore, this test SHOULD FAIL until we implement unique salting.
    assert hash_a != hash_b, "Hashes for the same password should be unique (salted)"
