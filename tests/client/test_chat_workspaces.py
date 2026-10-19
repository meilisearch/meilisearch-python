import pytest

from meilisearch.errors import MeilisearchApiError

WORKSPACE = "test-workspace"


@pytest.fixture
def chat_workspace(client):
    """Enable the chat completions feature and create a workspace."""
    client.update_experimental_features({"chatCompletions": True})
    client.update_chat_workspace_settings(WORKSPACE, {"source": "openAi", "apiKey": "test-key"})
    yield WORKSPACE
    try:
        client.delete_chat_workspace(WORKSPACE)
    except MeilisearchApiError:
        pass
    client.update_experimental_features({"chatCompletions": False})


def test_get_chat_workspace(client, chat_workspace):
    """Test that an existing workspace can be fetched."""
    assert client.get_chat_workspace(chat_workspace) == {"uid": chat_workspace}


def test_get_chat_workspace_not_found(client, chat_workspace):
    """Test that fetching an unknown workspace raises an API error."""
    with pytest.raises(MeilisearchApiError) as exc:
        client.get_chat_workspace("does-not-exist")
    assert exc.value.code == "chat_not_found"


def test_reset_chat_workspace_settings(client, chat_workspace):
    """Test that resetting settings removes the stored API key."""
    result = client.reset_chat_workspace_settings(chat_workspace)
    assert result["apiKey"] is None
    assert client.get_chat_workspace_settings(chat_workspace)["apiKey"] is None


def test_delete_chat_workspace(client, chat_workspace):
    """Test that a deleted workspace can no longer be fetched."""
    client.delete_chat_workspace(chat_workspace)
    with pytest.raises(MeilisearchApiError) as exc:
        client.get_chat_workspace(chat_workspace)
    assert exc.value.code == "chat_not_found"


@pytest.mark.parametrize(
    "method",
    ["get_chat_workspace", "delete_chat_workspace", "reset_chat_workspace_settings"],
)
@pytest.mark.parametrize("uid", ["", "a/b", "a\\b"])
def test_chat_workspace_methods_reject_invalid_uid(client, method, uid):
    """Test that an empty uid or one with path separators is rejected before any request."""
    with pytest.raises(ValueError):
        getattr(client, method)(uid)
