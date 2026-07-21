"""Tests for dynamic search rule endpoints."""

from copy import deepcopy

import pytest

from meilisearch.errors import MeilisearchApiError
from meilisearch.models.task import TaskInfo

pytestmark = pytest.mark.usefixtures("enable_dynamic_search_rules")

RULE_OPTIONS = {
    "description": "Black Friday products",
    "precedence": 10,
    "active": True,
    "conditions": {"query": {"words": "black friday"}},
    "actions": [
        {
            "selector": {"indexUid": "products", "id": "123"},
            "action": {"type": "pin", "position": 1},
        }
    ],
}


def _upsert_and_wait(client, uid, options):
    task = client.update_dynamic_search_rule(uid, options)
    client.wait_for_task(task.task_uid)
    return task


def test_get_dynamic_search_rules_with_pagination_and_filters(client):
    _upsert_and_wait(client, "black-friday", RULE_OPTIONS)

    inactive_options = deepcopy(RULE_OPTIONS)
    inactive_options.update({"description": "Archived promotion", "active": False})
    _upsert_and_wait(client, "archived-promotion", inactive_options)

    all_rules = client.get_dynamic_search_rules()
    assert all_rules.total == 2

    first_page = client.get_dynamic_search_rules({"offset": 0, "limit": 1})
    assert first_page.offset == 0
    assert first_page.limit == 1
    assert first_page.total == 2
    assert len(first_page.results) == 1

    filtered = client.get_dynamic_search_rules(
        {"filter": {"query": "Black Friday", "active": True}}
    )
    assert filtered.total == 1
    assert filtered.results[0].uid == "black-friday"


def test_get_dynamic_search_rule(client):
    _upsert_and_wait(client, "black-friday", RULE_OPTIONS)

    rule = client.get_dynamic_search_rule("black-friday")

    assert rule.uid == "black-friday"
    assert rule.description == RULE_OPTIONS["description"]
    assert rule.precedence == RULE_OPTIONS["precedence"]
    assert rule.actions == RULE_OPTIONS["actions"]


def test_update_dynamic_search_rule_creates_rule_and_returns_task(client):
    task = client.update_dynamic_search_rule(
        "black-friday", RULE_OPTIONS, metadata="create promotion"
    )

    assert isinstance(task, TaskInfo)
    assert task.status == "enqueued"
    assert task.type == "dsrUpdate"

    completed_task = client.wait_for_task(task.task_uid)
    assert completed_task.custom_metadata == "create promotion"
    assert client.get_dynamic_search_rule("black-friday").description == "Black Friday products"


def test_update_dynamic_search_rule_updates_rule_and_returns_task(client):
    _upsert_and_wait(client, "black-friday", RULE_OPTIONS)

    task = client.update_dynamic_search_rule(
        "black-friday",
        {"description": "Black Friday and Cyber Monday", "precedence": 5},
    )

    assert isinstance(task, TaskInfo)
    assert task.status == "enqueued"

    client.wait_for_task(task.task_uid)
    updated_rule = client.get_dynamic_search_rule("black-friday")
    assert updated_rule.description == "Black Friday and Cyber Monday"
    assert updated_rule.precedence == 5
    assert updated_rule.actions == RULE_OPTIONS["actions"]


def test_delete_dynamic_search_rule_returns_task(client):
    _upsert_and_wait(client, "black-friday", RULE_OPTIONS)

    task = client.delete_dynamic_search_rule("black-friday", metadata="remove promotion")

    assert isinstance(task, TaskInfo)
    assert task.status == "enqueued"
    assert task.type == "dsrUpdate"

    completed_task = client.wait_for_task(task.task_uid)
    assert completed_task.custom_metadata == "remove promotion"
    with pytest.raises(MeilisearchApiError):
        client.get_dynamic_search_rule("black-friday")
