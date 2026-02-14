from fastapi import APIRouter, Depends, Request

from api.deps import get_user_service, get_current_user
from api.limiter import limiter
from schemas.user import User, UserCreate
from services.user_service import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=User)
@limiter.limit("10/minute")
async def register(
    request: Request, user: UserCreate, service: UserService = Depends(get_user_service)
):
    return await service.new_user(user.username, user.password)


@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
