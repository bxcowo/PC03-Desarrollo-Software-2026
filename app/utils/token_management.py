import base64
import hashlib
import hmac
import json
from app.config import settings
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, UTC

def hash_password(password: str) -> str:
    return hmac.new(
        settings.SECRET_KEY.encode(),
        password.encode(),
        hashlib.sha256,
    ).hexdigest()


def create_token(ciudadano_id: str, email: str) -> str:
    payload = {
        "ciudadano_id": ciudadano_id,
        "email": email,
        "iat": datetime.now(UTC).isoformat()
    }
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode()
    payload_b64 = base64.urlsafe_b64encode(payload_bytes).rstrip(b"=").decode()

    sig = hmac.new(
        settings.SECRET_KEY.encode(),
        payload_b64.encode(),
        hashlib.sha256,
    ).hexdigest()

    return f"{payload_b64}.{sig}"


def decode_token(token: str) -> dict:
    try:
        payload_b64, sig = token.rsplit(".", 1)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token mal formado.",
        )

    expected_sig = hmac.new(
        settings.SECRET_KEY.encode(),
        payload_b64.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(sig, expected_sig):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firma del token inválida.",
        )

    padding = 4 - len(payload_b64) % 4
    payload_b64_padded = payload_b64 + "=" * (padding % 4)
    payload = json.loads(base64.urlsafe_b64decode(payload_b64_padded))
    return payload

_bearer = HTTPBearer()

def get_current_ciudadano_id(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> str:
    payload = decode_token(credentials.credentials)
    return payload["ciudadano_id"]
