import pytest

from core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from services.auth_service import AuthService
from services.user_service import UserService


async def test_create_user_success(session):
    service = UserService(session)
    user = await service.new_user("testuser", "securepass")
    assert user.username == "testuser"
    assert user.id is not None


async def test_create_user_duplicate(session):
    service = UserService(session)
    await service.new_user("dupe", "123")
    with pytest.raises(UserAlreadyExistsError):
        await service.new_user("dupe", "456")


async def test_authenticate_success(session):
    await UserService(session).new_user("loginme", "1234")
    access, refresh, token_type = await AuthService(session).authenticate(
        "loginme", "1234"
    )
    assert access and refresh
    assert token_type == "bearer"


async def test_authenticate_wrong_password(session):
    await UserService(session).new_user("wrongpass", "pass")
    with pytest.raises(InvalidCredentialsError):
        await AuthService(session).authenticate("wrongpass", "wrong")
