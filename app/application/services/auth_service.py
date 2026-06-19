"""
AuthService — orchestrates authentication use cases.

Depends on:
  - IUserRepository (injected, not imported directly)
  - security utilities from core/

This service knows NOTHING about:
  - MongoDB (that's infrastructure)
  - HTTP (that's the API layer)
  - FastAPI (never import it here)

TODO (you implement — one step at a time):
  1. register(): hash password, check for existing email, persist User
  2. login(): look up by email, verify password, issue tokens
  3. refresh(): validate refresh token (from Redis), issue new access token
  4. logout(): invalidate refresh token in Redis

Interview question to consider:
  "Why do we store refresh tokens in Redis and not MongoDB?"
  Hint: think about expiration, invalidation speed, and read patterns.
"""

from app.core.exceptions import AuthenticationError, AlreadyExistsError
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.domain.entities.user import User
from app.domain.interfaces.user_repository import IUserRepository


class AuthService:
    def __init__(self, user_repo: IUserRepository) -> None:
        self._user_repo = user_repo

    async def register(self, email: str, password: str) -> User:
        user_exists = await self._user_repo.get_by_email(email)
        if user_exists:
            raise AlreadyExistsError("User", email)
        hashed_password = hash_password(password)
        new_user = await self._user_repo.create(User(email, hashed_password))
        return new_user

    async def login(self, email: str, password: str) -> tuple[str, str]:
        user = await self._user_repo.get_by_email(email)
        if not user:
            raise AuthenticationError("Wrong email or password")
        if not verify_password(password, user.hashed_password):
            raise AuthenticationError("Wrong email or password")
        return (create_access_token(str(user.id)), create_refresh_token(str(user.id)))

    async def refresh(self, refresh_token: str) -> str:
        """Returns new access_token."""
        raise NotImplementedError

    async def logout(self, refresh_token: str) -> None:
        raise NotImplementedError
