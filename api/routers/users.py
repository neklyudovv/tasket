from fastapi import APIRouter, Depends, Request

from api.deps import get_user_service
from api.limiter import limiter
from api.security import create_access_token, create_refresh_token, decode_token
from core.exceptions import InvalidCredentialsError
from schemas.token import Token, TokenRefreshRequest
from schemas.user import User, UserCreate
from services.user_service import UserService


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
    request: Request, user: UserCreate, service: UserService = Depends(get_user_service)
):
    if await service.login_user(user.username, user.password):
        return Token(
            access_token=create_access_token({"sub": user.username}),
            refresh_token=create_refresh_token({"sub": user.username}),
            token_type="bearer",
        )
    raise InvalidCredentialsError


@router.post("/refresh", response_model=Token)
@limiter.limit("10/minute")
async def refresh_token(
    request: Request,
    refresh_req: TokenRefreshRequest,
    service: UserService = Depends(get_user_service),
):
    try:
        payload = decode_token(refresh_req.refresh_token)
        username: str = payload.get("sub")
        token_type: str = payload.get("type")

        if username is None or token_type != "refresh":
            raise InvalidCredentialsError
    except Exception:
        raise InvalidCredentialsError

    user = await service.get_user_by_username(username)
    if not user:
        raise InvalidCredentialsError

    return Token(
        access_token=create_access_token({"sub": username}),
        refresh_token=create_refresh_token({"sub": username}),
        token_type="bearer",
    )
