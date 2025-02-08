# pylint: disable=invalid-name

import pytest

from meilisearch.models.task import TaskInfo
from tests import common


def test_get_tasks_default(client):
    """Tests getting the global tasks list."""
    tasks = client.get_tasks()
    assert len(tasks.results) >= 1


def test_get_tasks(client, empty_index):
    """Tests getting the global tasks list after populating an index."""
    current_tasks = client.get_tasks()
    pre_count = current_tasks.from_
    empty_index()
    tasks = client.get_tasks()
    assert tasks.from_ == pre_count + 1


def test_get_tasks_empty_parameters(client):
    """Tests getting the global tasks list after populating an index."""
    tasks = client.get_tasks({})
    assert isinstance(tasks.results, list)


def test_get_tasks_with_parameters(client, empty_index):
    """Tests getting the global tasks list after populating an index."""
    empty_index()
    tasks = client.get_tasks({"limit": 1})
    assert len(tasks.results) == 1


def test_get_tasks_with_all_plural_parameters(client, empty_index):
    """Tests getting the global tasks list after populating an index."""
    empty_index()
    tasks = client.get_tasks(
        {"indexUids": [common.INDEX_UID], "statuses": ["succeeded"], "types": ["indexCreation"]}
    )
    assert len(tasks.results) >= 1


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
    assert len(tasks.results) > 1


def test_get_tasks_with_index_uid(client, empty_index):
    """Tests getting the global tasks list after populating an index."""
    empty_index()
    tasks = client.get_tasks({"limit": 1, "indexUids": [common.INDEX_UID]})
    assert len(tasks.results) == 1


def test_get_task(client):
    """Tests getting the tasks list of an empty index."""
    response = client.create_index(uid=common.INDEX_UID)
    client.wait_for_task(response.task_uid)
    task = client.get_task(response.task_uid)
    task_dict = task.__dict__
    assert "uid" in task_dict
    assert "index_uid" in task_dict
    assert "status" in task_dict
    assert "type" in task_dict
    assert "duration" in task_dict
    assert "enqueued_at" in task_dict
    assert "finished_at" in task_dict
    assert "details" in task_dict
    assert "started_at" in task_dict


def test_get_task_inexistent(client):
    """Tests getting a task that does not exists."""
    with pytest.raises(Exception):
        client.get_task("abc")


@pytest.fixture
def create_tasks(empty_index, small_movies):
    """Ensures there are some tasks present for testing."""
    index = empty_index()
    index.update_ranking_rules(["typo", "exactness"])
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
    assert "uids" in tasks.results[0].details["originalFilter"]
    assert "uids=1%2C2" in tasks.results[0].details["originalFilter"]


@pytest.mark.usefixtures("create_tasks")
def test_cancel_every_task(client):
    """Tests cancel every task."""
    task = client.cancel_tasks({"statuses": ["enqueued", "processing"]})
    client.wait_for_task(task.task_uid)
    tasks = client.get_tasks({"types": "taskCancelation"})

    assert isinstance(task, TaskInfo)
    assert task.task_uid is not None
    assert task.index_uid is None
    assert task.type == "taskCancelation"
    assert "statuses=enqueued%2Cprocessing" in tasks.results[0].details["originalFilter"]


def test_delete_tasks_by_uid(client, empty_index, small_movies):
    """Tests getting a task of an inexistent operation."""
    index = empty_index()
    task_addition = index.add_documents(small_movies)
    task_deleted = client.delete_tasks({"uids": task_addition.task_uid})
    client.wait_for_task(task_deleted.task_uid)
    with pytest.raises(Exception):
        client.get_task(task_addition.task_uid)
    task = client.get_task(task_deleted.task_uid)

    assert isinstance(task_deleted, TaskInfo)
    assert task_deleted.task_uid is not None
    assert task_deleted.index_uid is None
    assert task_deleted.type == "taskDeletion"
    assert "uids" in task.details["originalFilter"]
    assert f"uids={task_addition.task_uid}" in task.details["originalFilter"]


def test_delete_tasks_by_filter(client):
    task = client.delete_tasks({"statuses": ["succeeded", "failed", "canceled"]})
    client.wait_for_task(task.task_uid)
    tasks_after = client.get_tasks()

    assert isinstance(task, TaskInfo)
    assert task.task_uid is not None
    assert task.index_uid is None
    assert task.type == "taskDeletion"
    assert len(tasks_after.results) >= 1
    assert (
        "statuses=succeeded%2Cfailed%2Ccanceled" in tasks_after.results[0].details["originalFilter"]
    )


@pytest.mark.usefixtures("create_tasks")
def test_get_tasks_in_reverse(client):
    """Tests getting the global tasks list in reverse."""
    tasks = client.get_tasks({})
    reverse_tasks = client.get_tasks({"reverse": "true"})

    assert reverse_tasks.results[0] == tasks.results[-1]


def test_get_batches_default(client):
    """Tests getting the batches."""
    batches = client.get_batches()
    assert len(batches.results) >= 1


@pytest.mark.usefixtures("create_tasks")
def test_get_batches_with_parameters(client):
    """Tests getting batches with a parameter (empty or otherwise)."""
    rev_batches = client.get_batches({"reverse": "true"})
    batches = client.get_batches({})

    assert len(batches.results) > 1
    assert rev_batches.results[0].uid == batches.results[-1].uid


def test_get_batch(client):
    """Tests getting the details of a batch."""
    batches = client.get_batches({"limit": 1})
    batch = client.get_batch(batches.results[0].uid)
    batch_dict = batch.__dict__
    assert "uid" in batch_dict
    assert "details" in batch_dict
    assert "stats" in batch_dict
    assert "duration" in batch_dict
    assert "started_at" in batch_dict
    assert "finished_at" in batch_dict
    assert "progress" in batch_dict
