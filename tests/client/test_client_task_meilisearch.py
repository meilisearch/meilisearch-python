# pylint: disable=invalid-name

import pytest
from tests import common

def test_get_tasks_default(client):
    """Tests getting the global tasks list."""
    tasks = client.get_tasks()
    assert isinstance(tasks, dict)
    assert 'results' in tasks

def test_get_tasks(client, empty_index):
    """Tests getting the global tasks list after populating an index."""
    current_tasks = client.get_tasks()
    pre_count = current_tasks["from"]
    empty_index()
    tasks = client.get_tasks()
    assert isinstance(tasks, dict)
    assert tasks['from'] == pre_count + 1

def test_get_tasks_empty_parameters(client, empty_index):
    """Tests getting the global tasks list after populating an index."""
    tasks = client.get_tasks({})
    assert isinstance(tasks, dict)
    assert isinstance(tasks['results'], list)

def test_get_tasks_with_parameters(client):
    """Tests getting the global tasks list after populating an index."""
    tasks = client.get_tasks({'limit': 1, 'from': 1})
    assert isinstance(tasks, dict)
    assert len(tasks['results']) == 1
    assert tasks['results'][0]['uid'] == 1

def test_get_tasks_with_index_uid(client):
    """Tests getting the global tasks list after populating an index."""
    tasks = client.get_tasks({'limit': 1, 'indexUid': [common.INDEX_UID]})
    assert isinstance(tasks, dict)
    assert len(tasks['results']) == 1

def test_get_task(client):
    """Tests getting the tasks list of an empty index."""
    response = client.create_index(uid=common.INDEX_UID)
    client.wait_for_task(response['taskUid'])
    task = client.get_task(response['taskUid'])
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
