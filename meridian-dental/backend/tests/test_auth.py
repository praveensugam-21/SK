import pytest
from datetime import timedelta
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.dependencies import require_role

def test_password_hashing():
    raw_pwd = "SecretClinicPassword@2026"
    hashed = hash_password(raw_pwd)
    
    assert hashed != raw_pwd
    assert verify_password(raw_pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_generation_and_decoding():
    payload = {"sub": "123e4567-e89b-12d3-a456-426614174000", "role": "dentist"}
    token = create_access_token(payload, expires_delta=timedelta(minutes=15))
    
    assert isinstance(token, str)
    decoded = decode_token(token)
    assert decoded["sub"] == payload["sub"]
    assert decoded["role"] == "dentist"
    assert "exp" in decoded

def test_refresh_token():
    payload = {"sub": "123e4567-e89b-12d3-a456-426614174000"}
    token = create_refresh_token(payload)
    
    decoded = decode_token(token)
    assert decoded["sub"] == payload["sub"]

def test_require_role_helper():
    checker_list = require_role(["admin", "dentist"])
    assert callable(checker_list)
    
    checker_varargs = require_role("admin", "dentist")
    assert callable(checker_varargs)
