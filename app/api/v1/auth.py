"""
Auth endpoints.

TODO (you implement):
  POST /auth/register  → RegisterRequest → UserResponse
  POST /auth/login     → LoginRequest → TokenResponse
  POST /auth/refresh   → body: {refresh_token} → TokenResponse
  POST /auth/logout    → body: {refresh_token} → 204

Each handler should be thin:
  - Validate input (Pydantic does this automatically)
  - Call the service
  - Map service result to response schema
  - Never put business logic here

Question to think about:
  Where should refresh tokens be passed — in the request body or as an
  HTTP-only cookie? What are the security tradeoffs?
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_auth_service
from app.application.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse, RefreshRequest
from app.application.services.auth_service import AuthService
from app.core.exceptions import AuthenticationError, AlreadyExistsError

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
        body: RegisterRequest,
        auth_service: AuthService = Depends(get_auth_service)
):
    try:
        user = await auth_service.register(body.email, body.password)
    except AlreadyExistsError:
        raise HTTPException(status_code=409, detail="User with this email already exists")  # ✅
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(
        body: LoginRequest,
        auth_service: AuthService = Depends(get_auth_service)
):
    try:
        access_t, refresh_t = await auth_service.login(body.email, body.password)
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(
        access_token=access_t,
        refresh_token=refresh_t,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
        body: RefreshRequest,
        auth_service: AuthService = Depends(get_auth_service)
):
    try:
        access_token = await auth_service.refresh(body.refresh_token)
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    return TokenResponse(access_token=access_token, refresh_token=body.refresh_token)


@router.post("/logout", status_code=204)
async def logout(
        body: RefreshRequest,
        auth_service: AuthService = Depends(get_auth_service)
):
    await auth_service.logout(body.refresh_token)
