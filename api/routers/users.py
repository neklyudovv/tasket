from fastapi import APIRouter, Depends, Request

from api.deps import get_user_service, get_token_service
from api.limiter import limiter
from core.exceptions import InvalidCredentialsError
from schemas.token import Token, TokenRefreshRequest
from schemas.user import User, UserCreate
from services.user_service import UserService
from services.token_service import TokenService


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=User)
@limiter.limit("10/minute")
async def register(
    request: Request, user: UserCreate, service: UserService = Depends(get_user_service)
):
    return await service.new_user(user.username, user.password)


@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
async def login(
    request: Request,
    user: UserCreate,
    user_service: UserService = Depends(get_user_service),
    token_service: TokenService = Depends(get_token_service),
):

    authenticated_user = await user_service.login_user(user.username, user.password)
    access, refresh, token_type = await token_service.create_tokens_for_user(authenticated_user)
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
    token_service: TokenService = Depends(get_token_service),
):
    try:
        new_access, new_refresh, token_type = await token_service.refresh(refresh_req.refresh_token)
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
    token_service: TokenService = Depends(get_token_service),
):
    await token_service.logout(refresh_req.refresh_token)
    return {"message": "Successfully logged out"}
