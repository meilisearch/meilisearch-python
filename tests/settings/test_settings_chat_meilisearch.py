import pytest

DEFAULT_CHAT_SETTINGS_KEYS = {
    "description",
    "documentTemplate",
    "documentTemplateMaxBytes",
    "searchParameters",
}

NEW_CHAT_SETTINGS = {
    "description": "A collection of movies",
    "documentTemplate": "A movie titled {{ doc.title }}",
    "documentTemplateMaxBytes": 200,
    "searchParameters": {"limit": 5},
}


@pytest.fixture
def chat_completions_enabled(client):
    """Updating index chat settings requires the chatCompletions experimental feature."""
    previous = client.get_experimental_features().get("chatCompletions", False)
    client.update_experimental_features({"chatCompletions": True})
    yield
    client.update_experimental_features({"chatCompletions": previous})


def test_get_chat_settings(empty_index):
    response = empty_index().get_chat_settings()

    assert DEFAULT_CHAT_SETTINGS_KEYS == set(response)
    assert response["description"] == ""
    assert response["documentTemplateMaxBytes"] == 400
    assert response["searchParameters"] == {}


def test_update_chat_settings(empty_index, chat_completions_enabled):
    index = empty_index()

    response = index.update_chat_settings(NEW_CHAT_SETTINGS)
    index.wait_for_task(response.task_uid)
    response = index.get_chat_settings()

    assert response == NEW_CHAT_SETTINGS


def test_update_chat_settings_partial(empty_index, chat_completions_enabled):
    index = empty_index()
    index.wait_for_task(index.update_chat_settings(NEW_CHAT_SETTINGS).task_uid)

    response = index.update_chat_settings({"description": "Updated"})
    index.wait_for_task(response.task_uid)
    response = index.get_chat_settings()

    assert response["description"] == "Updated"
    assert response["documentTemplate"] == NEW_CHAT_SETTINGS["documentTemplate"]
    assert response["searchParameters"] == NEW_CHAT_SETTINGS["searchParameters"]


def test_reset_chat_settings(empty_index, chat_completions_enabled):
    index = empty_index()
    default_settings = index.get_chat_settings()
    index.wait_for_task(index.update_chat_settings(NEW_CHAT_SETTINGS).task_uid)
    assert index.get_chat_settings() != default_settings

    response = index.reset_chat_settings()
    index.wait_for_task(response.task_uid)

    assert index.get_chat_settings() == default_settings
