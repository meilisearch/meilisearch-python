# pylint: disable=redefined-outer-name

from meilisearch.models.index import CompositeEmbedder, HuggingFaceEmbedder, OpenAiEmbedder, UserProvidedEmbedder
import pytest


def test_get_default_embedders(empty_index):
    """Tests getting default embedders."""
    response = empty_index().get_embedders()

    assert response is None


def test_update_embedders_with_user_provided_source(new_embedders, empty_index):
    """Tests updating embedders."""
    index = empty_index()
    response_update = index.update_embedders(new_embedders)
    update = index.wait_for_task(response_update.task_uid)
    response_get = index.get_embedders()
    assert update.status == "succeeded"
    assert isinstance(response_get.embedders["default"], UserProvidedEmbedder)
    assert isinstance(response_get.embedders["open_ai"], OpenAiEmbedder)


def test_reset_embedders(new_embedders, empty_index):
    """Tests resetting the typo_tolerance setting to its default value."""
    index = empty_index()

    # Update the settings
    response_update = index.update_embedders(new_embedders)
    update1 = index.wait_for_task(response_update.task_uid)
    assert update1.status == "succeeded"
    # Get the setting after update
    response_get = index.get_embedders()
    assert isinstance(response_get.embedders["default"], UserProvidedEmbedder)
    assert isinstance(response_get.embedders["open_ai"], OpenAiEmbedder)
    # Reset the setting
    response_reset = index.reset_embedders()
    update2 = index.wait_for_task(response_reset.task_uid)
    # Get the setting after reset
    assert update2.status == "succeeded"
    assert isinstance(response_get.embedders["default"], UserProvidedEmbedder)
    assert isinstance(response_get.embedders["open_ai"], OpenAiEmbedder)
    response_last = index.get_embedders()
    assert response_last is None


@pytest.mark.usefixtures("enable_composite_embedders")
def test_composite_embedders_configurable(empty_index):
    """Tests composite embedders."""
    index = empty_index()

    hf_model = HuggingFaceEmbedder().model_dump(by_alias=True, exclude_none=True)

    # create composite embedder
    composite_spec = {
        "default": {
            "source": "composite",
            "searchEmbedder": hf_model,
            "indexingEmbedder": hf_model,
        }
    }

    response_update = index.update_embedders(composite_spec)
    update = index.wait_for_task(response_update.task_uid)
    response_get = index.get_embedders()
    assert update.status == "succeeded"

    embedder = response_get.embedders["default"]
    assert isinstance(embedder, CompositeEmbedder)
    assert isinstance(embedder.search_embedder, HuggingFaceEmbedder)
    assert isinstance(embedder.indexing_embedder, HuggingFaceEmbedder)
