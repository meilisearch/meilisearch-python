# pylint: disable=invalid-name

import pytest
from tests import common

def test_get_tasks_default(empty_index):
    """Tests getting the tasks list of an empty index."""
    task = empty_index().get_tasks()
    assert isinstance(task, dict)
    assert 'results' in task
    assert len(task['results']) != 0

def test_get_tasks(empty_index, small_movies):
    """Tests getting the tasks list of a populated index."""
    index = empty_index()
    current_tasks = index.get_tasks()
    pre_count = current_tasks["from"]
    response = index.add_documents(small_movies)
    assert 'taskUid' in response
    tasks = index.get_tasks()
    assert tasks["from"] == pre_count + 1

def test_get_task(client):
    """Tests getting a task of a operation."""
    task = client.create_index(uid=common.INDEX_UID)
    client.wait_for_task(task['taskUid'])
    index = client.get_index(uid=common.INDEX_UID)
    task = index.get_task(task['taskUid'])
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

def test_get_task_inexistent(empty_index):
    """Tests getting a task of an inexistent operation."""
    with pytest.raises(Exception):
        empty_index().get_task('abc')
