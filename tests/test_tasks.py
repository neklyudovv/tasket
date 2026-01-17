from datetime import UTC, datetime, timedelta
import pytest

from core.exceptions import PermissionDeniedError, TaskNotFoundError
from services.task_service import TaskService


async def test_create_and_get_task(session):
    service = TaskService(session)
    user_id = 1
    due = datetime.now(UTC) + timedelta(days=1)

    task = await service.create_task("Test Task", user_id, due)
    assert task.title == "Test Task"
    assert task.user_id == user_id
    assert task.is_done is False

    tasks = await service.get_user_tasks(user_id)
    assert len(tasks) == 1
    assert tasks[0].id == task.id


async def test_done_task_success(session):
    service = TaskService(session)
    user_id = 2
    due = datetime.now(UTC) + timedelta(days=2)
    task = await service.create_task("Another Task", user_id, due)

    updated = await service.done_task(task.id, user_id)
    assert updated.is_done is True


async def test_done_task_permission_denied(session):
    service = TaskService(session)
    user_id = 3
    wrong_user_id = 999
    due = datetime.now(UTC) + timedelta(days=2)
    task = await service.create_task("Private Task", user_id, due)

    with pytest.raises(PermissionDeniedError):
        await service.done_task(task.id, wrong_user_id)


async def test_done_task_not_found(session):
    service = TaskService(session)
    with pytest.raises(TaskNotFoundError):
        await service.done_task("non-existent-id", 1)


async def test_delete_task_success(session):
    service = TaskService(session)
    user_id = 4
    due = datetime.now(UTC) + timedelta(days=3)
    task = await service.create_task("Delete Me", user_id, due)

    await service.delete_task(task.id, user_id)
    tasks = await service.get_user_tasks(user_id)
    assert len(tasks) == 0


async def test_delete_task_permission_denied(session):
    service = TaskService(session)
    user_id = 5
    wrong_user_id = 888
    due = datetime.now(UTC) + timedelta(days=3)
    task = await service.create_task("Can't Touch This", user_id, due)

    with pytest.raises(PermissionDeniedError):
        await service.delete_task(task.id, wrong_user_id)


async def test_delete_task_not_found(session):
    service = TaskService(session)
    with pytest.raises(TaskNotFoundError):
        await service.delete_task("non-existent-id", 1)


async def test_pagination(session):
    service = TaskService(session)
    user_id = 10
    due = datetime.now(UTC) + timedelta(days=1)

    t1 = await service.create_task("Task 1", user_id, due)
    t2 = await service.create_task("Task 2", user_id, due)
    t3 = await service.create_task("Task 3", user_id, due)

    tasks = await service.get_user_tasks(user_id, limit=1)
    assert len(tasks) == 1
    assert tasks[0].id == t3.id

    tasks = await service.get_user_tasks(user_id, limit=1, offset=1)
    assert len(tasks) == 1
    assert tasks[0].id == t2.id

    tasks = await service.get_user_tasks(user_id, limit=1, offset=2)
    assert len(tasks) == 1
    assert tasks[0].id == t1.id


async def test_create_task_with_description(session):
    service = TaskService(session)
    user_id = 99

    task = await service.create_task(
        title="Desc Task",
        user_id=user_id,
        description="This is a test description"
    )
    assert task.description == "This is a test description"
    assert task.title == "Desc Task"

    task_empty = await service.create_task(
        title="No Desc Task",
        user_id=user_id,
    )
    assert task_empty.title == "No Desc Task"
    assert task_empty.description is None
