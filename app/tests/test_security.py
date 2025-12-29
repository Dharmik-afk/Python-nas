import pytest
import hashlib
from app.core.security import hasher

def test_get_copyparty_hash_raw():
    # Known values from copyparty --ah-gen "password" --ah-alg sha2,424242
    password = "password"
    expected = "+_UbIhavqWiVaZ4F_pGUNUnQ4nDohEX00"
    actual = hasher.get_copyparty_hash(password)
    assert actual == expected

def test_get_internal_proxy_password():
    password = "password"
    expected = hashlib.sha256(password.encode()).hexdigest()
    actual = hasher.get_internal_proxy_password(password)
    assert actual == expected

def test_full_copyparty_hash_flow():
    password = "password"
    internal = hasher.get_internal_proxy_password(password)
    actual = hasher.get_copyparty_hash(internal)
    
    # SHA-256 of "password" is 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
    # copyparty --ah-gen "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
    # yielded +Yko0pFIbAzrOf9QALx5TYuP8xWfiBsB8
    assert actual == "+Yko0pFIbAzrOf9QALx5TYuP8xWfiBsB8"