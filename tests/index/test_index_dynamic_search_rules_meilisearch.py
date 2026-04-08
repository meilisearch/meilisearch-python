import pytest
from meilisearch.errors import MeilisearchApiError


@pytest.fixture
def test_index(client_with_index):
    index = client_with_index()
    yield index
    index.delete()


def test_list_dynamic_search_rules(test_index):
    """Test listing dynamic search rules"""
    response = test_index.list_dynamic_search_rules()
    assert isinstance(response, dict)
    assert "results" in response or "meta" in response
    if "results" in response:
        assert isinstance(response["results"], list)


def test_get_dynamic_search_rule(test_index):
    """Test getting a single dynamic search rule"""
    rule_uid = "test-rule-1"
    rule_body = {
        "conditions": [
            {
                "scope": ["title"],
                "operator": "contains",
                "value": "new"
            }
        ],
        "actions": [
            {
                "action": "promote",
                "documentIds": ["1"],
                "matchCondition": "all",
                "position": 1
            }
        ]
    }

    create_response = test_index.upsert_dynamic_search_rule(rule_uid, rule_body)
    test_index.wait_for_task(create_response.task_uid)

    response = test_index.get_dynamic_search_rule(rule_uid)
    assert isinstance(response, dict)
    assert response.get("uid") == rule_uid


def test_upsert_dynamic_search_rule(test_index):
    """Test creating or updating a dynamic search rule"""
    rule_uid = "test-rule-2"
    rule_body = {
        "conditions": [
            {
                "scope": ["title"],
                "operator": "contains",
                "value": "hello"
            }
        ],
        "actions": [
            {
                "action": "promote",
                "documentIds": ["2"],
                "matchCondition": "all",
                "position": 1
            }
        ]
    }

    response = test_index.upsert_dynamic_search_rule(rule_uid, rule_body)
    assert response.task_uid is not None

    test_index.wait_for_task(response.task_uid)

    retrieved = test_index.get_dynamic_search_rule(rule_uid)
    assert retrieved.get("uid") == rule_uid


def test_delete_dynamic_search_rule(test_index):
    """Test deleting a dynamic search rule"""
    rule_uid = "test-rule-3"
    rule_body = {
        "conditions": [
            {
                "scope": ["title"],
                "operator": "contains",
                "value": "delete-me"
            }
        ],
        "actions": [
            {
                "action": "promote",
                "documentIds": ["3"],
                "matchCondition": "all",
                "position": 1
            }
        ]
    }

    create_response = test_index.upsert_dynamic_search_rule(rule_uid, rule_body)
    test_index.wait_for_task(create_response.task_uid)

    delete_response = test_index.delete_dynamic_search_rule(rule_uid)
    assert delete_response.task_uid is not None

    test_index.wait_for_task(delete_response.task_uid)

    with pytest.raises(MeilisearchApiError):
        test_index.get_dynamic_search_rule(rule_uid)


def test_upsert_dynamic_search_rule_index_isolation(client_with_index):
    """Test that upsert on one index does not affect another index"""
    index_a = client_with_index()
    index_b = client_with_index()

    rule_uid = "isolation-rule"
    body_a = {
        "conditions": [
            {"scope": ["title"], "operator": "contains", "value": "foo"}
        ],
        "actions": [
            {"action": "promote", "documentIds": ["1"], "matchCondition": "all", "position": 1}
        ],
    }
    body_b = {
        "conditions": [
            {"scope": ["title"], "operator": "contains", "value": "bar"}
        ],
        "actions": [
            {"action": "promote", "documentIds": ["2"], "matchCondition": "all", "position": 2}
        ],
    }

    try:
        task_a = index_a.upsert_dynamic_search_rule(rule_uid, body_a)
        index_a.wait_for_task(task_a.task_uid)

        task_b = index_b.upsert_dynamic_search_rule(rule_uid, body_b)
        index_b.wait_for_task(task_b.task_uid)

        rule_a = index_a.get_dynamic_search_rule(rule_uid)
        rule_b = index_b.get_dynamic_search_rule(rule_uid)

        assert rule_a.get("uid") == rule_uid
        assert rule_b.get("uid") == rule_uid
        # Rules should be independent per index
        assert rule_a != rule_b
    finally:
        index_a.delete()
        index_b.delete()
