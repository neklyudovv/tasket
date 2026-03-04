import pytest

from core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from repositories import RefreshTokenRepository, UserRepository
from services.auth_service import AuthService
from services.user_service import UserService


def make_user_service(session):
    return UserService(UserRepository(session))


def make_auth_service(session):
    return AuthService(UserRepository(session), RefreshTokenRepository(session))


async def test_create_user_success(session):
    service = make_user_service(session)
    user = await service.new_user("testuser", "securepass")
    assert user.username == "testuser"
    assert user.id is not None


async def test_create_user_duplicate(session):
    service = make_user_service(session)
    await service.new_user("dupe", "123")
    with pytest.raises(UserAlreadyExistsError):
        await service.new_user("dupe", "456")


async def test_authenticate_success(session):
    await make_user_service(session).new_user("loginme", "1234")
    access, refresh, token_type = await make_auth_service(session).authenticate(
        "loginme", "1234"
    )
    assert access and refresh
    assert token_type == "bearer"


async def test_authenticate_wrong_password(session):
    await make_user_service(session).new_user("wrongpass", "pass")
    with pytest.raises(InvalidCredentialsError):
        await make_auth_service(session).authenticate("wrongpass", "wrong")
