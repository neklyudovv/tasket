import pytest
from core.user_service import new_user, login_user
from core.exceptions import UserAlreadyExistsError, InvalidCredentialsError


async def test_create_user_success(session):
    user = await new_user("testuser", "securepass", session)
    assert user["username"] == "testuser"
    assert "id" in user


async def test_create_user_duplicate(session):
    await new_user("dupe", "123", session)
    with pytest.raises(UserAlreadyExistsError):
        await new_user("dupe", "456", session)


async def test_login_user_success(session):
    await new_user("loginme", "1234", session)
    user = await login_user("loginme", "1234", session)
    assert user["username"] == "loginme"


async def test_login_user_wrong_password(session):
    await new_user("wrongpass", "pass", session)
    with pytest.raises(InvalidCredentialsError):
        await login_user("wrongpass", "wrong", session)
