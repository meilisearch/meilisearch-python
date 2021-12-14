# pylint: disable=invalid-name

import pytest
from tests import common

def test_get_tasks_default(client):
    """Tests getting the global tasks list."""
    tasks = client.get_tasks()
    assert isinstance(tasks, dict)
    assert len(tasks) == 1
    assert len(tasks['results']) != 0

def test_get_tasks(client, empty_index, small_movies):
    """Tests getting the global tasks list after populated an index."""
    index = empty_index()
    response = index.add_documents(small_movies)
    assert 'uid' in response
    response = index.add_documents(small_movies)
    assert 'uid' in response
    tasks = client.get_tasks()
    assert len(tasks) == 1
    assert len(tasks['results']) != 0

def test_get_task(client):
    """Tests getting the tasks list of an empty index."""
    response = client.create_index(uid=common.INDEX_UID)
    client.wait_for_task(response['uid'])
    task = client.get_task(response['uid'])
    assert isinstance(task, dict)
    assert len(task) == 9
    assert 'uid' in task
    assert 'status' in task
    assert 'type' in task
    assert 'duration' in task
    assert 'enqueuedAt' in task
    assert 'finishedAt' in task

def test_get_task_inexistent(client):
    """Tests getting a task of an inexistent operation."""
    with pytest.raises(Exception):
        client.get_task('999')
