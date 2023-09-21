import pytest

from meilisearch.models.index import Faceting

DEFAULT_MAX_VALUE_PER_FACET = 100
DEFAULT_SORT_FACET_VALUES_BY = {"*": "alpha"}
NEW_MAX_VALUE_PER_FACET = {"maxValuesPerFacet": 200}


def test_get_faceting_settings(empty_index):
    response = empty_index().get_faceting_settings()

    assert DEFAULT_MAX_VALUE_PER_FACET == response.max_values_per_facet
    assert DEFAULT_SORT_FACET_VALUES_BY == response.sort_facet_values_by


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


@pytest.mark.parametrize(
    "index_name, facet_order, max_values_per_facet, expected",
    [
        ("*", "alpha", 17, {"max_values_per_facet": 17, "sort_facet_values_by": {"*": "alpha"}}),
        ("*", "count", 41, {"max_values_per_facet": 41, "sort_facet_values_by": {"*": "count"}}),
        (
            "movies",
            "alpha",
            42,
            {"max_values_per_facet": 42, "sort_facet_values_by": {"*": "alpha", "movies": "alpha"}},
        ),
        (
            "movies",
            "alpha",
            73,
            {"max_values_per_facet": 73, "sort_facet_values_by": {"*": "alpha", "movies": "alpha"}},
        ),
    ],
)
def test_update_faceting_sort_facet_values(
    index_name, facet_order, max_values_per_facet, expected, empty_index
):
    faceting = Faceting(
        max_values_per_facet=max_values_per_facet,
        sort_facet_values_by={index_name: facet_order},
    )
    index = empty_index()
    response = index.update_faceting_settings(faceting.model_dump(by_alias=True))
    index.wait_for_task(response.task_uid)
    response = index.get_faceting_settings()
    assert response.model_dump() == expected


def test_reset_faceting(empty_index):
    index = empty_index()
    response = index.update_faceting_settings(
        {"maxValuesPerFacet": 17, "sortFacetValuesBy": {"*": "count"}}
    )
    index.wait_for_task(response.task_uid)
    response = index.reset_faceting_settings()
    index.wait_for_task(response.task_uid)
    response = index.get_faceting_settings()
    assert response == Faceting(
        max_values_per_facet=DEFAULT_MAX_VALUE_PER_FACET,
        sort_facet_values_by=DEFAULT_SORT_FACET_VALUES_BY,
    )
