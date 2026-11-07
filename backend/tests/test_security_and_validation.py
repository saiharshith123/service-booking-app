from datetime import datetime, timedelta, timezone
import pytest
from pydantic import ValidationError
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.schemas import SlotCreate

def test_password_hash_round_trip():
    hashed = hash_password("StrongPassword123!")
    assert hashed != "StrongPassword123!"
    assert verify_password("StrongPassword123!", hashed)
    assert not verify_password("wrong-password", hashed)

def test_jwt_contains_user_subject():
    token = create_access_token("42")
    payload = decode_access_token(token)
    assert payload["sub"] == "42"

def test_slot_rejects_end_before_start():
    start = datetime.now(timezone.utc) + timedelta(days=1)
    with pytest.raises(ValidationError):
        SlotCreate(service_name="Consultation", starts_at=start, ends_at=start - timedelta(minutes=30))
