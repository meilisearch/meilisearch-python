# pylint: disable=invalid-name

import pytest
from tests import common

def test_get_tasks_default(empty_index):
    """Tests getting the tasks list of an empty index."""
    task = empty_index().get_tasks()
    assert isinstance(task, dict)
    assert len(task) == 1
    assert len(task['results']) == 1

def test_get_tasks(empty_index, small_movies):
    """Tests getting the tasks list of a populated index."""
    index = empty_index()
    response = index.add_documents(small_movies)
    assert 'uid' in response
    response = index.add_documents(small_movies)
    assert 'uid' in response
    assert 'status' in response
    task = index.get_tasks()
    assert len(task) == 1
    assert len(task['results']) > 2

def test_get_task(client):
    """Tests getting a task of a operation."""
    task = client.create_index(uid=common.INDEX_UID)
    client.wait_for_task(task['uid'])
    index = client.get_index(uid=common.INDEX_UID)
    task = index.get_task(task['uid'])
    assert isinstance(task, dict)
    assert len(task) == 9
    assert 'uid' in task
    assert 'status' in task
    assert 'type' in task
    assert 'duration' in task
    assert 'enqueuedAt' in task
    assert 'finishedAt' in task

def test_get_task_inexistent(empty_index):
    """Tests getting a task of an inexistent operation."""
    with pytest.raises(Exception):
        empty_index().get_task('999')
