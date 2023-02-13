DEFAULT_MAX_VALUE_PER_FACET = 100
NEW_MAX_VALUE_PER_FACET = {"maxValuesPerFacet": 200}


def test_get_faceting_settings(empty_index):
    response = empty_index().get_faceting_settings()

    assert DEFAULT_MAX_VALUE_PER_FACET == response.max_values_per_facet


def test_update_faceting_settings(empty_index):
    index = empty_index()
    response = index.update_faceting_settings(NEW_MAX_VALUE_PER_FACET)
    index.wait_for_task(response.task_uid)
    response = index.get_faceting_settings()
    assert NEW_MAX_VALUE_PER_FACET["maxValuesPerFacet"] == response.max_values_per_facet


def test_delete_faceting_settings(empty_index):
    index = empty_index()
    response = index.update_faceting_settings(NEW_MAX_VALUE_PER_FACET)
    index.wait_for_task(response.task_uid)

    response = index.reset_faceting_settings()
    index.wait_for_task(response.task_uid)
    response = index.get_faceting_settings()
    assert DEFAULT_MAX_VALUE_PER_FACET == response.max_values_per_facet
