# pylint: disable=invalid-name

import pytest
from tests import common

def test_get_tasks_default(index_with_documents):
    """Tests getting the tasks list of an empty index."""
    tasks = index_with_documents().get_tasks()
    assert isinstance(tasks, dict)
    assert 'results' in tasks
    assert len(tasks['results']) != 0

def test_get_tasks(empty_index, small_movies):
    """Tests getting the tasks list of a populated index."""
    index = empty_index("test_task")
    current_tasks = index.get_tasks()
    pre_count = len(current_tasks['results'])
    response = index.add_documents(small_movies)
    assert 'taskUid' in response
    index.wait_for_task(response['taskUid'])
    tasks = index.get_tasks()
    assert len(tasks['results']) == pre_count + 1

def test_get_tasks_with_parameters(empty_index):
    """Tests getting the tasks list of a populated index."""
    index = empty_index()
    tasks = index.get_tasks({'limit': 1})
    assert isinstance(tasks, dict)
    assert len(tasks['results']) == 1

def test_get_tasks_with_index_uid(empty_index):
    """Tests getting the tasks list of a populated index."""
    index = empty_index()
    tasks = index.get_tasks({'limit': 1, 'indexUid': [common.INDEX_UID]})
    assert isinstance(tasks, dict)
    assert len(tasks['results']) == 1

def test_get_tasks_empty_parameters(empty_index):
    """Tests getting the global tasks list after populating an index."""
    index = empty_index()
    tasks = index.get_tasks({})
    assert isinstance(tasks, dict)
    assert isinstance(tasks['results'], list)

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
