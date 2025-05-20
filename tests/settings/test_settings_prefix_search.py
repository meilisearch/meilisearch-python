from meilisearch.models.index import PrefixSearch

DEFAULT_PREFIX_SEARCH_SETTINGS = PrefixSearch.INDEXING_TIME


def test_get_prefix_search(empty_index):
    response = empty_index().get_prefix_search()

    assert DEFAULT_PREFIX_SEARCH_SETTINGS == response


def test_update_prefix_search(empty_index):
    index = empty_index()

    response = index.update_prefix_search(PrefixSearch.DISABLED)
    index.wait_for_task(response.task_uid)
    response = index.get_prefix_search()
    assert PrefixSearch.DISABLED == response

    response = index.update_prefix_search(PrefixSearch.INDEXING_TIME)
    index.wait_for_task(response.task_uid)
    response = index.get_prefix_search()
    assert PrefixSearch.INDEXING_TIME == response


def test_reset_prefix_search(empty_index):
    index = empty_index()

    response = index.update_prefix_search(PrefixSearch.DISABLED)
    index.wait_for_task(response.task_uid)
    response = index.get_prefix_search()
    assert PrefixSearch.DISABLED == response
    assert DEFAULT_PREFIX_SEARCH_SETTINGS != response

    response = index.reset_prefix_search()
    index.wait_for_task(response.task_uid)
    response = index.get_prefix_search()
    assert DEFAULT_PREFIX_SEARCH_SETTINGS == response
