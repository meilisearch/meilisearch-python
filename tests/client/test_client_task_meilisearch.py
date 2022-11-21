# pylint: disable=invalid-name

import pytest

from meilisearch.models.task import TaskInfo
from tests import common


def test_get_tasks_default(client):
    """Tests getting the global tasks list."""
    tasks = client.get_tasks()
    assert isinstance(tasks, dict)
    assert "results" in tasks


def test_get_tasks(client, empty_index):
    """Tests getting the global tasks list after populating an index."""
    current_tasks = client.get_tasks()
    pre_count = current_tasks["from"]
    empty_index()
    tasks = client.get_tasks()
    assert isinstance(tasks, dict)
    assert tasks["from"] == pre_count + 1


def test_get_tasks_empty_parameters(client):
    """Tests getting the global tasks list after populating an index."""
    tasks = client.get_tasks({})
    assert isinstance(tasks, dict)
    assert isinstance(tasks["results"], list)


def test_get_tasks_with_parameters(client, empty_index):
    """Tests getting the global tasks list after populating an index."""
    empty_index()
    tasks = client.get_tasks({"limit": 1})
    assert isinstance(tasks, dict)
    assert len(tasks["results"]) == 1


def test_get_tasks_with_all_plural_parameters(client, empty_index):
    """Tests getting the global tasks list after populating an index."""
    empty_index()
    tasks = client.get_tasks(
        {"indexUids": [common.INDEX_UID], "statuses": ["succeeded"], "types": ["indexCreation"]}
    )
    assert isinstance(tasks, dict)
    assert len(tasks["results"]) > 1


def test_get_tasks_with_date_parameters(client, empty_index):
    """Tests getting the global tasks list after populating an index."""
    empty_index()
    tasks = client.get_tasks(
        {
            "beforeEnqueuedAt": "2042-04-02T00:42:42Z",
            "beforeStartedAt": "2042-04-02T00:42:42Z",
            "beforeFinishedAt": "2042-04-02T00:42:42Z",
        }
    )
    assert isinstance(tasks, dict)
    assert len(tasks["results"]) > 1


def test_get_tasks_with_index_uid(client, empty_index):
    """Tests getting the global tasks list after populating an index."""
    empty_index()
    tasks = client.get_tasks({"limit": 1, "indexUids": [common.INDEX_UID]})
    assert isinstance(tasks, dict)
    assert len(tasks["results"]) == 1


def test_get_task(client):
    """Tests getting the tasks list of an empty index."""
    response = client.create_index(uid=common.INDEX_UID)
    client.wait_for_task(response["taskUid"])
    task = client.get_task(response["taskUid"])
    assert isinstance(task, dict)
    assert len(task) == 11
    assert "uid" in task
    assert "indexUid" in task
    assert "status" in task
    assert "type" in task
    assert "duration" in task
    assert "enqueuedAt" in task
    assert "finishedAt" in task
    assert "details" in task
    assert "startedAt" in task


def test_get_task_inexistent(client):
    """Tests getting a task that does not exists."""
    with pytest.raises(Exception):
        client.get_task("abc")


@pytest.fixture
def create_tasks(empty_index, small_movies):
    """Ensures there are some tasks present for testing."""
    index = empty_index()
    index.update_ranking_rules(["type", "exactness"])
    index.reset_ranking_rules()
    index.add_documents(small_movies)
    index.add_documents(small_movies)

@pytest.mark.usefixtures("create_tasks")
def test_cancel_tasks(client):
    """Tests cancel a task with uid 1."""
    task = client.cancel_tasks({"uids": ["1", "2"]})
    client.wait_for_task(task.task_uid)
    tasks = client.get_tasks({"types": "taskCancelation"})

    assert isinstance(task, TaskInfo)
    assert task.task_uid is not None
    assert task.index_uid is None
    assert task.type == "taskCancelation"
    assert "uids" in tasks["results"][0]["details"]["originalFilter"]
    assert "uids=1%2C2" in tasks["results"][0]["details"]["originalFilter"]


def test_cancel_every_task(client):
    """Tests cancel every task."""
    task = client.cancel_tasks({"statuses": ["enqueued", "processing"]})
    client.wait_for_task(task.task_uid)
    tasks = client.get_tasks({"types": "taskCancelation"})

    assert isinstance(task, TaskInfo)
    assert task.task_uid is not None
    assert task.index_uid is None
    assert task.type == "taskCancelation"
    assert "statuses=enqueued%2Cprocessing" in tasks["results"][0]["details"]["originalFilter"]
