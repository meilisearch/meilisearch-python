# pylint: disable=invalid-name

import pytest
from tests import common

def test_get_tasks_default(client):
    """Tests getting the global tasks list."""
    tasks = client.get_tasks()
    assert isinstance(tasks, dict)
    assert 'results' in tasks

def test_get_tasks(client, empty_index):
    """Tests getting the global tasks list after populated an index."""
    current_tasks = client.get_tasks()
    pre_count = len(current_tasks["results"])
    empty_index()
    tasks = client.get_tasks()
    assert isinstance(tasks, dict)
    assert len(tasks['results']) == pre_count + 1

def test_get_task(client):
    """Tests getting the tasks list of an empty index."""
    response = client.create_index(uid=common.INDEX_UID)
    client.wait_for_task(response['uid'])
    task = client.get_task(response['uid'])
    assert isinstance(task, dict)
    assert len(task) == 9
    assert 'uid' in task
    assert 'indexUid' in task
    assert 'status' in task
    assert 'type' in task
    assert 'duration' in task
    assert 'enqueuedAt' in task
    assert 'finishedAt' in task
    assert 'details' in task
    assert 'startedAt' in task

def test_get_task_inexistent(client):
    """Tests getting a task that does not exists."""
    with pytest.raises(Exception):
        client.get_task('abc')
