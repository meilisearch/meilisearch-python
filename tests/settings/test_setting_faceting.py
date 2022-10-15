DEFAULT_MAX_VALUE_PER_FACET = 100
NEW_MAX_VALUE_PER_FACET = {"maxValuesPerFacet": 200}


def test_get_faceting_settings(empty_index):
    response = empty_index().get_faceting_settings()

    assert isinstance(response, dict)
    assert {"maxValuesPerFacet": DEFAULT_MAX_VALUE_PER_FACET} == response


def test_update_faceting_settings(empty_index):
    index = empty_index()
    response = index.update_faceting_settings(NEW_MAX_VALUE_PER_FACET)
    assert isinstance(response, dict)
    assert "taskUid" in response

    index.wait_for_task(response["taskUid"])
    response = index.get_faceting_settings()
    assert isinstance(response, dict)
    assert NEW_MAX_VALUE_PER_FACET == response


def test_delete_faceting_settings(empty_index):
    index = empty_index()
    response = index.reset_faceting_settings()

    index.wait_for_task(response["taskUid"])
    response = index.get_faceting_settings()
    assert isinstance(response, dict)
    assert {"maxValuesPerFacet": DEFAULT_MAX_VALUE_PER_FACET} == response
