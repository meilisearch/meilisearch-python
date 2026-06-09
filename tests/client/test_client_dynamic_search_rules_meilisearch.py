"""Tests for dynamic search rule management endpoints."""

import pytest

from meilisearch.errors import MeilisearchApiError

pytestmark = pytest.mark.usefixtures("enable_dynamic_search_rules")


def test_get_dynamic_search_rules_empty(client):
    """Test getting dynamic search rules when none exist."""
    rules = client.get_dynamic_search_rules()
    assert rules.results is not None
    assert isinstance(rules.results, list)
    assert len(rules.results) == 0


def test_create_or_update_dynamic_search_rule(client):
    """Test creating a dynamic search rule."""
    rule_data = {
        "description": "Test rule for promotion",
        "priority": 10,
        "active": True,
        "conditions": [{"scope": "query", "isEmpty": True}],
        "actions": [
            {
                "selector": {"indexUid": "movies", "id": "123"},
                "action": {"type": "pin", "position": 1},
            }
        ],
    }

    rule = client.create_or_update_dynamic_search_rule("test-rule", rule_data)

    assert rule.uid == "test-rule"
    assert rule.description == rule_data["description"]
    assert rule.priority == 10
    assert rule.active is True


def test_get_dynamic_search_rule(client):
    """Test getting a single dynamic search rule."""
    # Create a rule first
    rule_data = {
        "description": "Test rule",
        "active": True,
    }

    created_rule = client.create_or_update_dynamic_search_rule("test-rule", rule_data)

    # Get the rule
    rule = client.get_dynamic_search_rule(created_rule.uid)

    assert rule.uid == created_rule.uid
    assert rule.description == rule_data["description"]


def test_get_dynamic_search_rule_not_found(client):
    """Test getting a dynamic search rule that doesn't exist."""
    with pytest.raises(MeilisearchApiError):
        client.get_dynamic_search_rule("non-existent-uid")


def test_update_dynamic_search_rule(client):
    """Test updating a dynamic search rule."""
    # Create a rule first
    rule_data = {
        "description": "Original description",
        "priority": 10,
        "active": True,
        "conditions": [{"scope": "query", "isEmpty": True}],
        "actions": [
            {
                "selector": {"indexUid": "movies", "id": "123"},
                "action": {"type": "pin", "position": 1},
            }
        ],
    }

    created_rule = client.create_or_update_dynamic_search_rule("test-rule", rule_data)

    # Update the rule
    update_data = {
        "description": "Updated description",
        "priority": 5,
    }

    updated_rule = client.create_or_update_dynamic_search_rule(created_rule.uid, update_data)

    assert updated_rule.uid == created_rule.uid
    assert updated_rule.description == update_data["description"]
    assert updated_rule.priority == 5


def test_delete_dynamic_search_rule(client):
    """Test deleting a dynamic search rule."""
    # Create a rule first
    rule_data = {
        "description": "Rule to delete",
        "active": True,
    }

    created_rule = client.create_or_update_dynamic_search_rule("test-rule", rule_data)

    # Delete the rule
    status_code = client.delete_dynamic_search_rule(created_rule.uid)

    assert status_code == 204

    # Verify it's deleted
    with pytest.raises(MeilisearchApiError):
        client.get_dynamic_search_rule(created_rule.uid)


def test_delete_dynamic_search_rule_not_found(client):
    """Test deleting a dynamic search rule that doesn't exist."""
    with pytest.raises(MeilisearchApiError):
        client.delete_dynamic_search_rule("non-existent-uid")
