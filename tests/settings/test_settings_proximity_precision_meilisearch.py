from meilisearch.models.index import ProximityPrecision

NEW_PROXIMITY_PRECISION = ProximityPrecision.BY_ATTRIBUTE


def test_get_proximity_precision(empty_index):
    """Tests getting default proximity precision."""
    response = empty_index().get_proximity_precision()
    assert response == ProximityPrecision.BY_WORD


def test_update_proximity_precision(empty_index):
    """Tests updating proximity precision."""
    index = empty_index()
    response = index.update_proximity_precision(NEW_PROXIMITY_PRECISION)
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    response = index.get_proximity_precision()
    assert NEW_PROXIMITY_PRECISION == response


def test_reset_proximity_precision(empty_index):
    """Tests resetting the proximity precision to its default value."""
    index = empty_index()
    # Update the settings first
    response = index.update_proximity_precision(NEW_PROXIMITY_PRECISION)
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    # Check the settings have been correctly updated
    response = index.get_proximity_precision()
    assert NEW_PROXIMITY_PRECISION == response
    # Check the reset of the settings
    response = index.reset_proximity_precision()
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    response = index.get_proximity_precision()
    assert response == ProximityPrecision.BY_WORD
