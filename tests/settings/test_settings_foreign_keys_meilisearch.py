FOREIGN_KEYS = [
    {"foreignIndexUid": "authors", "fieldName": "author"},
]


def test_get_foreign_keys(empty_index, enable_foreign_keys):
    """Tests getting the foreign keys."""
    response = empty_index().get_foreign_keys()
    assert response == []


def test_update_foreign_keys(empty_index, enable_foreign_keys):
    """Tests updating the foreign keys."""
    index = empty_index()
    response = index.update_foreign_keys(FOREIGN_KEYS)
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"

    get_keys = index.get_foreign_keys()
    assert len(get_keys) == len(FOREIGN_KEYS)
    for key in FOREIGN_KEYS:
        assert key in get_keys


def test_update_foreign_keys_to_none(empty_index, enable_foreign_keys):
    """Tests updating the foreign keys at null."""
    index = empty_index()
    # Update the settings first
    response = index.update_foreign_keys(FOREIGN_KEYS)
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    # Check the settings have been correctly updated
    get_keys = index.get_foreign_keys()
    for key in FOREIGN_KEYS:
        assert key in get_keys
    # Launch test to update at null the setting
    response = index.update_foreign_keys(None)
    index.wait_for_task(response.task_uid)
    response = index.get_foreign_keys()
    assert response == []


def test_reset_foreign_keys(empty_index, enable_foreign_keys):
    """Tests resetting the foreign keys setting to its default value"""
    index = empty_index()
    # Update the settings first
    response = index.update_foreign_keys(FOREIGN_KEYS)
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    # Check the settings have been correctly updated
    get_keys = index.get_foreign_keys()
    assert len(get_keys) == len(FOREIGN_KEYS)
    for key in FOREIGN_KEYS:
        assert key in get_keys
    # Check the reset of the settings
    response = index.reset_foreign_keys()
    index.wait_for_task(response.task_uid)
    response = index.get_foreign_keys()
    assert response == []
