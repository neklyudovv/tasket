import pytest


async def test_root_not_found(client):
    response = await client.get("/")
    assert response.status_code == 404


async def test_create_user(client):
    response = await client.post(
        "/users/register", json={"username": "apiuser", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "apiuser"
    assert "id" in data


async def test_login_and_create_task(client):
    await client.post(
        "/users/register", json={"username": "taskuser", "password": "taskpass"}
    )

    login_res = await client.post(
        "/auth/login", json={"username": "taskuser", "password": "taskpass"}
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    task_res = await client.post(
        "/tasks/",
        json={"title": "Integration Task", "due_date": "2025-12-31T23:59:59Z"},
        headers=headers,
    )
    assert task_res.status_code == 200
    task_data = task_res.json()
    assert task_data["title"] == "Integration Task"

    list_res = await client.get("/tasks/", headers=headers)
    assert list_res.status_code == 200
    tasks = list_res.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_data["id"]
