import pytest
from datetime import datetime, timedelta, UTC
from core.task_service import create_task, get_user_tasks, done_task, delete_task
from core.exceptions import TaskNotFoundError, PermissionDeniedError


async def test_create_and_get_task(session):
    user_id = 1
    due = datetime.now(UTC) + timedelta(days=1)

    task = await create_task("Test Task", user_id, session, due)
    assert task.title == "Test Task"
    assert task.user_id == user_id
    assert task.is_done is False

    tasks = await get_user_tasks(user_id, session)
    assert len(tasks) == 1
    assert tasks[0].id == task.id


async def test_done_task_success(session):
    user_id = 2
    due = datetime.now(UTC) + timedelta(days=2)
    task = await create_task("Another Task", user_id, session, due)

    updated = await done_task(task.id, user_id, session)
    assert updated.is_done is True


async def test_done_task_permission_denied(session):
    user_id = 3
    wrong_user_id = 999
    due = datetime.now(UTC) + timedelta(days=2)
    task = await create_task("Private Task", user_id, session, due)

    with pytest.raises(PermissionDeniedError):
        await done_task(task.id, wrong_user_id, session)


async def test_done_task_not_found(session):
    with pytest.raises(TaskNotFoundError):
        await done_task("non-existent-id", 1, session)


async def test_delete_task_success(session):
    user_id = 4
    due = datetime.now(UTC) + timedelta(days=3)
    task = await create_task("Delete Me", user_id, session, due)

    await delete_task(task.id, user_id, session)
    tasks = await get_user_tasks(user_id, session)
    assert len(tasks) == 0


async def test_delete_task_permission_denied(session):
    user_id = 5
    wrong_user_id = 888
    due = datetime.now(UTC) + timedelta(days=3)
    task = await create_task("Can't Touch This", user_id, session, due)

    with pytest.raises(PermissionDeniedError):
        await delete_task(task.id, wrong_user_id, session)


async def test_delete_task_not_found(session):
    with pytest.raises(TaskNotFoundError):
        await delete_task("non-existent-id", 1, session)


async def test_pagination(session):
    user_id = 10
    due = datetime.now(UTC) + timedelta(days=1)
    
    t1 = await create_task("Task 1", user_id, session, due)
    t2 = await create_task("Task 2", user_id, session, due)
    t3 = await create_task("Task 3", user_id, session, due)
    
    tasks = await get_user_tasks(user_id, session, limit=1)
    assert len(tasks) == 1
    assert tasks[0].id == t3.id
    
    tasks = await get_user_tasks(user_id, session, limit=1, offset=1)
    assert len(tasks) == 1
    assert tasks[0].id == t2.id
    
    tasks = await get_user_tasks(user_id, session, limit=1, offset=2)
    assert len(tasks) == 1
    assert tasks[0].id == t1.id
