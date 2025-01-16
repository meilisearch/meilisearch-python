from typing import List

from meilisearch.models.index import LocalizedAttributes

NEW_LOCALIZED_ATTRIBUTES = [{"attributePatterns": ["title"], "locales": ["eng"]}]


def unpack_loc_attrs_response(response: List[LocalizedAttributes]):
    return [loc_attrs.model_dump(by_alias=True) for loc_attrs in response]


def test_get_localized_attributes(empty_index):
    """Tests getting default localized_attributes."""
    response = empty_index().get_localized_attributes()
    assert response is None


def test_update_localized_attributes(empty_index):
    """Tests updating proximity precision."""
    index = empty_index()
    response = index.update_localized_attributes(NEW_LOCALIZED_ATTRIBUTES)
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    response = index.get_localized_attributes()
    assert NEW_LOCALIZED_ATTRIBUTES == unpack_loc_attrs_response(response)


def test_reset_localized_attributes(empty_index):
    """Tests resetting the proximity precision to its default value."""
    index = empty_index()
    # Update the settings first
    response = index.update_localized_attributes(NEW_LOCALIZED_ATTRIBUTES)
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    # Check the settings have been correctly updated
    response = index.get_localized_attributes()
    assert NEW_LOCALIZED_ATTRIBUTES == unpack_loc_attrs_response(response)
    # Check the reset of the settings
    response = index.reset_localized_attributes()
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    response = index.get_localized_attributes()
    assert response is None
