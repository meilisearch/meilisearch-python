# pylint: disable=redefined-outer-name
import pytest

from meilisearch.models.index import OpenAiEmbedder, UserProvidedEmbedder


@pytest.fixture
def new_settings(new_embedders):
    return {
        "rankingRules": ["typo", "words"],
        "searchableAttributes": ["title", "overview"],
        "embedders": new_embedders,
    }


DEFAULT_RANKING_RULES = ["words", "typo", "proximity", "attribute", "sort", "exactness"]

DEFAULT_TYPO_TOLERANCE = {
    "enabled": True,
    "minWordSizeForTypos": {
        "oneTypo": 5,
        "twoTypos": 9,
    },
    "disableOnWords": [],
    "disableOnAttributes": [],
}


def test_get_settings_default(empty_index):
    """Tests getting all settings by default."""
    response = empty_index().get_settings()
    for rule in DEFAULT_RANKING_RULES:
        assert rule in response["rankingRules"]
    for typo in DEFAULT_TYPO_TOLERANCE:  # pylint: disable=consider-using-dict-items
        assert typo in response["typoTolerance"]
        assert DEFAULT_TYPO_TOLERANCE[typo] == response["typoTolerance"][typo]
    assert response["distinctAttribute"] is None
    assert response["searchableAttributes"] == ["*"]
    assert response["displayedAttributes"] == ["*"]
    assert response["stopWords"] == []
    assert response["synonyms"] == {}


@pytest.mark.usefixtures("enable_vector_search")
def test_update_settings(new_settings, empty_index):
    """Tests updating some settings."""
    index = empty_index()
    response = index.update_settings(new_settings)
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    response = index.get_settings()
    for rule in new_settings["rankingRules"]:
        assert rule in response["rankingRules"]
    assert response["distinctAttribute"] is None
    for attribute in new_settings["searchableAttributes"]:
        assert attribute in response["searchableAttributes"]
    assert response["displayedAttributes"] == ["*"]
    assert response["stopWords"] == []
    assert response["synonyms"] == {}
    assert isinstance(response["embedders"]["default"], UserProvidedEmbedder)
    assert isinstance(response["embedders"]["open_ai"], OpenAiEmbedder)


@pytest.mark.usefixtures("enable_vector_search")
def test_reset_settings(new_settings, empty_index):
    """Tests resetting all the settings to their default value."""
    index = empty_index()
    # Update settings first
    response = index.update_settings(new_settings)
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    # Check the settings have been correctly updated
    response = index.get_settings()
    for rule in new_settings["rankingRules"]:
        assert rule in response["rankingRules"]
    assert response["distinctAttribute"] is None
    for attribute in new_settings["searchableAttributes"]:
        assert attribute in response["searchableAttributes"]
    assert response["displayedAttributes"] == ["*"]
    assert response["stopWords"] == []
    assert response["synonyms"] == {}
    # Check the reset of the settings
    response = index.reset_settings()
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    response = index.get_settings()
    for rule in DEFAULT_RANKING_RULES:
        assert rule in response["rankingRules"]
    for typo in DEFAULT_TYPO_TOLERANCE:  # pylint: disable=consider-using-dict-items
        assert typo in response["typoTolerance"]
        assert DEFAULT_TYPO_TOLERANCE[typo] == response["typoTolerance"][typo]
    assert response["distinctAttribute"] is None
    assert response["displayedAttributes"] == ["*"]
    assert response["searchableAttributes"] == ["*"]
    assert response["stopWords"] == []
    assert response["synonyms"] == {}
    assert response.get("embedders") is None
