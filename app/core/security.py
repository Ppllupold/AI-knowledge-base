"""
JWT creation/verification and password hashing utilities.

This module belongs in core/ (not infrastructure/) because security
is a cross-cutting concern used by both the API layer (deps.py)
and the application layer (AuthService).

TODO (you implement):
  - create_access_token(subject: str) -> str
  - create_refresh_token(subject: str) -> str
  - decode_token(token: str) -> dict
  - hash_password(password: str) -> str
  - verify_password(plain: str, hashed: str) -> bool
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import AuthenticationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    payload = {
        "sub": subject,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes),
        "type": "access"
    }
    return jwt.encode(payload, algorithm=settings.algorithm, key=settings.secret_key)


def create_refresh_token(subject: str) -> str:
    payload = {
        "sub": subject,
        "exp": datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days),
        "type": "refresh"
    }
    return jwt.encode(payload, key=settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, key=settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        raise AuthenticationError("Invalid or expired token")
    return payload
