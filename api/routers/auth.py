from fastapi import APIRouter, Depends, Request

from api.deps import get_auth_service
from api.limiter import limiter
from core.exceptions import InvalidCredentialsError
from schemas.token import Token, TokenRefreshRequest
from schemas.user import UserCreate
from services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
async def login(
    request: Request,
    user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    access, refresh, token_type = await auth_service.authenticate(
        user.username, user.password
    )
    return Token(
        access_token=access,
        refresh_token=refresh,
        token_type=token_type,
    )


@router.post("/refresh", response_model=Token)
@limiter.limit("10/minute")
async def refresh_token(
    request: Request,
    refresh_req: TokenRefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        new_access, new_refresh, token_type = await auth_service.refresh(refresh_req.refresh_token)
    except InvalidCredentialsError:
        raise
    return Token(
        access_token=new_access,
        refresh_token=new_refresh,
        token_type=token_type,
    )


@router.post("/logout")
async def logout(
    refresh_req: TokenRefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    await auth_service.logout(refresh_req.refresh_token)
    return {"message": "Successfully logged out"}
