NEW_SEARCH_CUTOFF_MS = 150


def test_get_search_cutoff_ms(empty_index):
    """Tests getting default search cutoff in ms."""
    response = empty_index().get_search_cutoff_ms()
    assert response is None


def test_update_search_cutoff_ms(empty_index):
    """Tests updating search cutoff in ms."""
    index = empty_index()
    response = index.update_search_cutoff_ms(NEW_SEARCH_CUTOFF_MS)
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    response = index.get_search_cutoff_ms()
    assert NEW_SEARCH_CUTOFF_MS == response


def test_reset_search_cutoff_ms(empty_index):
    """Tests resetting the search cutoff to its default value."""
    index = empty_index()
    # Update the settings first
    response = index.update_search_cutoff_ms(NEW_SEARCH_CUTOFF_MS)
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    # Check the settings have been correctly updated
    response = index.get_search_cutoff_ms()
    assert NEW_SEARCH_CUTOFF_MS == response
    # Check the reset of the settings
    response = index.reset_search_cutoff_ms()
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    response = index.get_search_cutoff_ms()
    assert response is None
