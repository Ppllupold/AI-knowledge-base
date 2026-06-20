"""
FastAPI dependency injection.

This file is the glue between the API layer and the application/infrastructure layers.
It constructs concrete service objects and injects them into route handlers.

Why here and not in main.py?
  Keeps main.py minimal. deps.py is the DI container equivalent in FastAPI.

TODO (you implement):
  - get_current_user(): decode JWT from Authorization header, load User from repo
  - get_auth_service(): build AuthService with a MongoUserRepository
  - get_search_service(): build SearchService with all its dependencies
  - get_ingestion_service(): similar

Pattern to follow:
  async def get_auth_service(
      request: Request,
  ) -> AuthService:
      db = request.app.state.mongo_db
      user_repo = MongoUserRepository(db)
      return AuthService(user_repo)
"""
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.application.services.auth_service import AuthService
from app.core.exceptions import AuthenticationError
from app.core.security import decode_token
from app.domain.entities.user import User
from app.infrastructure.db.client import get_database
from app.infrastructure.db.repositories.user_repository import MongoUserRepository

bearer_scheme = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> User:
    """
    Validate the Bearer JWT and return the authenticated User.
    Raises 401 if the token is invalid or expired.
    """
    db = get_database()
    user_repo = MongoUserRepository(db)
    try:
        payload = decode_token(credentials.credentials)
        user = await user_repo.get_by_id(UUID(payload["sub"]))
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except AuthenticationError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    return user


def get_auth_service() -> AuthService:
    db = get_database()
    repo = MongoUserRepository(db)
    return AuthService(repo)
