from datetime import UTC, datetime, timedelta
import pytest
import jwt

from core.config import settings
from api.security import create_refresh_token, decode_token


@pytest.mark.asyncio
async def test_login_returns_tokens(client, session):
    res = await client.post(
        "/users/register", json={"username": "authtest", "password": "password"}
    )
    assert res.status_code == 200

    res = await client.post(
        "/users/login", json={"username": "authtest", "password": "password"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_refresh_flow(client):
    await client.post(
        "/users/register", json={"username": "refreshtest", "password": "password"}
    )

    login_res = await client.post(
        "/users/login", json={"username": "refreshtest", "password": "password"}
    )
    refresh_token = login_res.json()["refresh_token"]
    access_token_1 = login_res.json()["access_token"]

    refresh_res = await client.post(
        "/users/refresh", json={"refresh_token": refresh_token}
    )
    assert refresh_res.status_code == 200
    new_data = refresh_res.json()
    assert "access_token" in new_data
    assert "refresh_token" in new_data


@pytest.mark.asyncio
async def test_invalid_refresh_token(client):
    res = await client.post(
        "/users/refresh", json={"refresh_token": "invalid.token.here"}
    )
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_expired_refresh_token(client):
    expired_data = {"sub": "test", "type": "refresh"}

    expired_time = datetime.now(UTC) - timedelta(days=1)
    token = jwt.encode(
        {"sub": "test", "type": "refresh", "exp": expired_time},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    res = await client.post("/users/refresh", json={"refresh_token": token})
    assert res.status_code == 401
