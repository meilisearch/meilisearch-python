# pylint: disable=invalid-name

DISPLAYED_ATTRIBUTES = ["id", "release_date", "title", "poster", "overview", "genre"]


def test_get_displayed_attributes(empty_index, small_movies):
    """Tests getting the displayed attributes before and after indexing a dataset."""
    index = empty_index()
    response = index.get_displayed_attributes()
    assert response == ["*"]
    response = index.add_documents(small_movies)
    index.wait_for_task(response.task_uid)
    get_attributes = index.get_displayed_attributes()
    assert get_attributes == ["*"]


def test_update_displayed_attributes(empty_index):
    """Tests updating the displayed attributes."""
    index = empty_index()
    response = index.update_displayed_attributes(DISPLAYED_ATTRIBUTES)
    index.wait_for_task(response.task_uid)
    get_attributes_new = index.get_displayed_attributes()
    assert len(get_attributes_new) == len(DISPLAYED_ATTRIBUTES)
    for attribute in DISPLAYED_ATTRIBUTES:
        assert attribute in get_attributes_new


def test_update_displayed_attributes_to_none(empty_index):
    """Tests updating the displayed attributes at null."""
    index = empty_index()
    # Update the settings first
    response = index.update_displayed_attributes(DISPLAYED_ATTRIBUTES)
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    # Check the settings have been correctly updated
    get_attributes = index.get_displayed_attributes()
    for attribute in DISPLAYED_ATTRIBUTES:
        assert attribute in get_attributes
    response = index.reset_displayed_attributes()
    index.wait_for_task(response.task_uid)
    response = index.get_displayed_attributes()
    assert response == ["*"]


def test_reset_displayed_attributes(empty_index):
    """Tests resetting the displayed attributes setting to its default value."""
    index = empty_index()
    # Update the settings first
    response = index.update_displayed_attributes(DISPLAYED_ATTRIBUTES)
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    # Check the settings have been correctly updated
    get_attributes_new = index.get_displayed_attributes()
    assert len(get_attributes_new) == len(DISPLAYED_ATTRIBUTES)
    for attribute in DISPLAYED_ATTRIBUTES:
        assert attribute in get_attributes_new
    # Check the reset of the settings
    response = index.reset_displayed_attributes()
    index.wait_for_task(response.task_uid)
    get_attributes = index.get_displayed_attributes()
    assert get_attributes == ["*"]
