import pytest
from core import new_user, login_user
from core import UserAlreadyExistsError, InvalidCredentialsError


@pytest.mark.asyncio
async def test_create_user_success(session):
    user = await new_user("testuser", "securepass", session)
    assert user["username"] == "testuser"
    assert "id" in user


@pytest.mark.asyncio
async def test_create_user_duplicate(session):
    await new_user("dupe", "123", session)
    with pytest.raises(UserAlreadyExistsError):
        await new_user("dupe", "456", session)


@pytest.mark.asyncio
async def test_login_user_success(session):
    await new_user("loginme", "1234", session)
    user = await login_user("loginme", "1234", session)
    assert user["username"] == "loginme"


@pytest.mark.asyncio
async def test_login_user_wrong_password(session):
    await new_user("wrongpass", "pass", session)
    with pytest.raises(InvalidCredentialsError):
        await login_user("wrongpass", "wrong", session)
