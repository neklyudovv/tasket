from fastapi import APIRouter, Depends, Request
from ..limiter import limiter
from schemas.user import UserCreate, User
from core.user_service import UserService
from ..deps import get_user_service
from ..security import create_access_token

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", response_model=User)
@limiter.limit("10/minute")
async def register(
    request: Request,
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return await service.new_user(user.username, user.password)


@router.post("/login")
@limiter.limit("10/minute")
async def login(
    request: Request,
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    if await service.login_user(user.username, user.password):
        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}