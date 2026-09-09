from datetime import datetime, timezone
from typing import Any, cast
from unittest.mock import Mock

import pytest

from meilisearch.client import Client
from meilisearch.errors import MeilisearchTaskFailedError, MeilisearchTimeoutError
from meilisearch.index import Index
from meilisearch.models.task import Task
from meilisearch.task import TaskHandler


def make_task(status: str, error: dict | None = None, uid: int = 42) -> Task:
    timestamp = datetime.now(timezone.utc)
    return Task(
        uid=uid,
        status=status,
        type="documentAddition",
        error=error,
        enqueuedAt=timestamp,
        startedAt=timestamp,
        finishedAt=timestamp if status not in ("enqueued", "processing") else None,
    )


def handler_with_tasks(*tasks: Task) -> TaskHandler:
    handler = cast(Any, TaskHandler.__new__(TaskHandler))
    handler.get_task = Mock(side_effect=tasks)
    return cast(TaskHandler, handler)


def test_wait_for_task_failed_preserves_default_behavior():
    task = make_task("failed", {"message": "bad document", "code": "invalid"})
    handler = handler_with_tasks(task)

    result = handler.wait_for_task(task.uid, interval_in_ms=0)

    assert result is task


def test_wait_for_task_failed_raises_and_retains_task():
    task = make_task("failed", {"message": "bad document", "code": "invalid"})
    handler = handler_with_tasks(task)

    with pytest.raises(MeilisearchTaskFailedError) as raised:
        handler.wait_for_task(task.uid, interval_in_ms=0, raise_on_failure=True)

    assert raised.value.task is task
    assert raised.value.uid == task.uid
    assert raised.value.error == task.error
    assert raised.value.message == "bad document"


def test_wait_for_task_failed_without_error_raises_useful_exception():
    task = make_task("failed", None)
    handler = handler_with_tasks(task)

    with pytest.raises(MeilisearchTaskFailedError, match="Task 42 failed"):
        handler.wait_for_task(task.uid, interval_in_ms=0, raise_on_failure=True)


def test_wait_for_task_failed_without_message_uses_fallback():
    task = make_task("failed", {"code": "invalid"})
    handler = handler_with_tasks(task)

    with pytest.raises(MeilisearchTaskFailedError) as raised:
        handler.wait_for_task(task.uid, interval_in_ms=0, raise_on_failure=True)

    assert raised.value.message == "Task 42 failed"


def test_wait_for_task_succeeded_with_raise_enabled_returns_task():
    task = make_task("succeeded")
    handler = handler_with_tasks(task)

    assert handler.wait_for_task(task.uid, interval_in_ms=0, raise_on_failure=True) is task


def test_wait_for_task_timeout_is_unchanged():
    handler = handler_with_tasks()

    with pytest.raises(MeilisearchTimeoutError):
        handler.wait_for_task(42, timeout_in_ms=0, raise_on_failure=True)

    handler.get_task.assert_not_called()


def test_wait_for_task_polls_until_failed_then_raises(monkeypatch):
    import meilisearch.task as task_module

    monkeypatch.setattr(task_module, "sleep", lambda _: None)
    processing = make_task("processing")
    failed = make_task("failed", {"code": "invalid"})
    handler = handler_with_tasks(processing, failed)

    with pytest.raises(MeilisearchTaskFailedError):
        handler.wait_for_task(42, timeout_in_ms=5000, raise_on_failure=True)

    assert handler.get_task.call_count == 2


def test_client_wait_for_task_forwards_raise_on_failure():
    client = Client.__new__(Client)
    client.task_handler = Mock()

    client.wait_for_task(42, 5000, 50, raise_on_failure=True)

    client.task_handler.wait_for_task.assert_called_once_with(
        42, 5000, 50, raise_on_failure=True
    )


def test_client_wait_for_task_preserves_legacy_default_forwarding():
    client = Client.__new__(Client)
    client.task_handler = Mock()

    client.wait_for_task(42, 5000, 50)

    client.task_handler.wait_for_task.assert_called_once_with(42, 5000, 50)


def test_index_wait_for_task_forwards_raise_on_failure():
    index = Index.__new__(Index)
    index.task_handler = Mock()

    index.wait_for_task(42, 5000, 50, raise_on_failure=True)

    index.task_handler.wait_for_task.assert_called_once_with(
        42, 5000, 50, raise_on_failure=True
    )


def test_index_wait_for_task_preserves_legacy_default_forwarding():
    index = Index.__new__(Index)
    index.task_handler = Mock()

    index.wait_for_task(42, 5000, 50)

    index.task_handler.wait_for_task.assert_called_once_with(42, 5000, 50)
