import pytest
from datetime import datetime, timedelta
from backend.core.task_service import create_task, get_user_tasks, done_task, delete_task
from backend.core.exceptions import TaskNotFoundError, PermissionDeniedError


@pytest.mark.asyncio
async def test_create_and_get_task(session):
    user_id = 1
    due = datetime.utcnow() + timedelta(days=1)

    task = await create_task("Test Task", due, user_id, session)
    assert task.title == "Test Task"
    assert task.user_id == user_id
    assert task.is_done is False

    tasks = await get_user_tasks(user_id, session)
    assert len(tasks) == 1
    assert tasks[0].id == task.id


@pytest.mark.asyncio
async def test_done_task_success(session):
    user_id = 2
    due = datetime.utcnow() + timedelta(days=2)
    task = await create_task("Another Task", due, user_id, session)

    updated = await done_task(task.id, user_id, session)
    assert updated.is_done is True


@pytest.mark.asyncio
async def test_done_task_permission_denied(session):
    user_id = 3
    wrong_user_id = 999
    due = datetime.utcnow() + timedelta(days=2)
    task = await create_task("Private Task", due, user_id, session)

    with pytest.raises(PermissionDeniedError):
        await done_task(task.id, wrong_user_id, session)


@pytest.mark.asyncio
async def test_done_task_not_found(session):
    with pytest.raises(TaskNotFoundError):
        await done_task("non-existent-id", 1, session)


@pytest.mark.asyncio
async def test_delete_task_success(session):
    user_id = 4
    due = datetime.utcnow() + timedelta(days=3)
    task = await create_task("Delete Me", due, user_id, session)

    await delete_task(task.id, user_id, session)
    tasks = await get_user_tasks(user_id, session)
    assert len(tasks) == 0


@pytest.mark.asyncio
async def test_delete_task_permission_denied(session):
    user_id = 5
    wrong_user_id = 888
    due = datetime.utcnow() + timedelta(days=3)
    task = await create_task("Can't Touch This", due, user_id, session)

    with pytest.raises(PermissionDeniedError):
        await delete_task(task.id, wrong_user_id, session)


@pytest.mark.asyncio
async def test_delete_task_not_found(session):
    with pytest.raises(TaskNotFoundError):
        await delete_task("non-existent-id", 1, session)
