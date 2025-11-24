"""Tests for webhook management endpoints."""

import pytest

from meilisearch.errors import MeilisearchApiError


def test_get_webhooks_empty(client):
    """Test getting webhooks when none exist."""
    webhooks = client.get_webhooks()
    assert webhooks.results is not None
    assert isinstance(webhooks.results, list)
    assert len(webhooks.results) == 0


def test_create_webhook(client):
    """Test creating a webhook."""
    webhook_data = {
        "url": "https://example.com/webhook",
        "headers": {
            "Authorization": "Bearer secret-token",
            "X-Custom-Header": "custom-value",
        },
    }

    webhook = client.create_webhook(webhook_data)

    assert webhook.uuid is not None
    assert webhook.url == webhook_data["url"]
    assert webhook.headers["X-Custom-Header"] == webhook_data["headers"]["X-Custom-Header"]


def test_get_webhook(client):
    """Test getting a single webhook."""
    # Create a webhook first
    webhook_data = {
        "url": "https://example.com/webhook",
    }

    created_webhook = client.create_webhook(webhook_data)

    # Get the webhook
    webhook = client.get_webhook(created_webhook.uuid)

    assert webhook.uuid == created_webhook.uuid
    assert webhook.url == webhook_data["url"]


def test_get_webhook_not_found(client):
    """Test getting a webhook that doesn't exist."""
    with pytest.raises(MeilisearchApiError):
        client.get_webhook("non-existent-uid")


def test_update_webhook(client):
    """Test updating a webhook."""
    # Create a webhook first
    webhook_data = {
        "url": "https://example.com/webhook",
    }

    created_webhook = client.create_webhook(webhook_data)

    # Update the webhook
    update_data = {
        "url": "https://example.com/updated-webhook",
    }

    updated_webhook = client.update_webhook(created_webhook.uuid, update_data)

    assert updated_webhook.uuid == created_webhook.uuid
    assert updated_webhook.url == update_data["url"]


def test_delete_webhook(client):
    """Test deleting a webhook."""
    # Create a webhook first
    webhook_data = {
        "url": "https://example.com/webhook",
    }

    created_webhook = client.create_webhook(webhook_data)

    # Delete the webhook
    status_code = client.delete_webhook(created_webhook.uuid)

    assert status_code == 204

    # Verify it's deleted
    with pytest.raises(MeilisearchApiError):
        client.get_webhook(created_webhook.uuid)


def test_delete_webhook_not_found(client):
    """Test deleting a webhook that doesn't exist."""
    with pytest.raises(MeilisearchApiError):
        client.delete_webhook("non-existent-uid")


def test_create_webhook_missing_required_fields(client):
    """Test creating a webhook without required fields."""
    # Missing 'url' field
    webhook_data = {
        "headers": {
            "Authorization": "Bearer secret-token",
        },
    }

    with pytest.raises(MeilisearchApiError):
        client.create_webhook(webhook_data)
