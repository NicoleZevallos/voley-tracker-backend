import pytest
from app.auth.jwt import verify_password, get_password_hash

def test_verify_correct_password():
    password = "test_password"
    hashed_password = get_password_hash(password)
    
    assert verify_password(password, hashed_password) is True

def test_verify_incorrect_password():
    password = "test_password"
    wrong_password = "wrong_password"
    hashed_password = get_password_hash(password)
    
    assert verify_password(wrong_password, hashed_password) is False
