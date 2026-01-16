import pytest
from services.user_service import UserService
from core.exceptions import UserAlreadyExistsError, InvalidCredentialsError


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


async def test_login_user_success(session):
    service = UserService(session)
    await service.new_user("loginme", "1234")
    user = await service.login_user("loginme", "1234")
    assert user.username == "loginme"


async def test_login_user_wrong_password(session):
    service = UserService(session)
    await service.new_user("wrongpass", "pass")
    with pytest.raises(InvalidCredentialsError):
        await service.login_user("wrongpass", "wrong")
