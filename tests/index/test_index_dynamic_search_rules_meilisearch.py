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
    # Create a rule first
    rule_uid = "test-rule-1"
    rule_body = {
        "condition": "query = 'new'",
        "match_condition": "all",
        "actions": [
            {
                "action": "promote",
                "document_ids": ["1"],
                "position": 1
            }
        ]
    }
    
    create_response = test_index.upsert_dynamic_search_rule(rule_uid, rule_body)
    test_index.wait_for_task(create_response.task_uid)
    
    # Now retrieve it
    response = test_index.get_dynamic_search_rule(rule_uid)
    assert isinstance(response, dict)
    assert response.get("uid") == rule_uid


def test_upsert_dynamic_search_rule(test_index):
    """Test creating or updating a dynamic search rule"""
    rule_uid = "test-rule-2"
    rule_body = {
        "condition": "query = 'hello'",
        "match_condition": "all",
        "actions": [
            {
                "action": "promote",
                "document_ids": ["2"],
                "position": 1
            }
        ]
    }
    
    response = test_index.upsert_dynamic_search_rule(rule_uid, rule_body)
    assert response.task_uid is not None
    
    test_index.wait_for_task(response.task_uid)
    
    # Verify it was created
    retrieved = test_index.get_dynamic_search_rule(rule_uid)
    assert retrieved.get("uid") == rule_uid


def test_delete_dynamic_search_rule(test_index):
    """Test deleting a dynamic search rule"""
    rule_uid = "test-rule-3"
    rule_body = {
        "condition": "query = 'delete-me'",
        "match_condition": "all",
        "actions": [
            {
                "action": "promote",
                "document_ids": ["3"],
                "position": 1
            }
        ]
    }
    
    # Create rule
    create_response = test_index.upsert_dynamic_search_rule(rule_uid, rule_body)
    test_index.wait_for_task(create_response.task_uid)
    
    # Delete it
    delete_response = test_index.delete_dynamic_search_rule(rule_uid)
    assert delete_response.task_uid is not None
    
    test_index.wait_for_task(delete_response.task_uid)
    
    # Verify it's deleted - should raise error or return empty
    with pytest.raises(MeilisearchApiError):
        test_index.get_dynamic_search_rule(rule_uid)
