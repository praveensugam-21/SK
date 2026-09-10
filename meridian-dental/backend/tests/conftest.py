import pytest
import sys
import os
from pathlib import Path

# Add backend to sys.path
backend_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_path))

from app.utils.security import hash_password, verify_password, create_access_token, decode_token
from app.config import settings

@pytest.fixture
def sample_user_data():
    return {
        "email": "testdentist@meridian.dental",
        "password": "SecurePassword123!",
        "role": "dentist",
        "full_name": "Dr. Anita Roy"
    }
