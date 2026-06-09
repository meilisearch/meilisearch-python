import re

import pytest

from meilisearch.models.index import SizeFormat

HUMAN_SIZE_PATTERN = re.compile(r"^\d+(\.\d+)?\s+(B|KiB|MiB|GiB|TiB)$")


@pytest.mark.usefixtures("indexes_sample")
def test_get_all_stats(client):
    """Tests getting all stats."""
    response = client.get_all_stats()
    assert isinstance(response, dict)
    assert "databaseSize" in response
    assert isinstance(response["databaseSize"], int)
    assert "lastUpdate" in response
    assert "indexes" in response
    assert "indexUID" in response["indexes"]
    assert "indexUID2" in response["indexes"]


@pytest.mark.usefixtures("indexes_sample")
def test_get_all_stats_with_internal_database_sizes(client):
    """Tests getting all stats with showInternalDatabaseSizes parameter."""
    response = client.get_all_stats(show_internal_database_sizes=True)
    assert isinstance(response, dict)
    assert isinstance(response["databaseSize"], int)
    assert any("internalDatabaseSizes" in index_stats for index_stats in response["indexes"].values())
    for index_stats in response["indexes"].values():
        if "internalDatabaseSizes" in index_stats:
            assert isinstance(index_stats["internalDatabaseSizes"], dict)
            assert len(index_stats["internalDatabaseSizes"]) > 0
            assert all(
                isinstance(value, int) for value in index_stats["internalDatabaseSizes"].values()
            )


@pytest.mark.usefixtures("indexes_sample")
def test_get_all_stats_with_size_format(client):
    """Tests getting all stats with sizeFormat parameter."""
    response = client.get_all_stats(
        show_internal_database_sizes=True,
        size_format=SizeFormat.HUMAN,
    )
    assert isinstance(response, dict)
    assert isinstance(response["databaseSize"], str)
    assert HUMAN_SIZE_PATTERN.match(response["databaseSize"])
    assert any(
        "internalDatabaseSizes" in index_stats for index_stats in response["indexes"].values()
    )
    for index_stats in response["indexes"].values():
        if "internalDatabaseSizes" in index_stats:
            assert all(
                isinstance(value, str) and HUMAN_SIZE_PATTERN.match(value)
                for value in index_stats["internalDatabaseSizes"].values()
            )


@pytest.mark.usefixtures("indexes_sample")
def test_get_all_stats_with_all_params(client):
    """Tests getting all stats with both query parameters."""
    response = client.get_all_stats(
        show_internal_database_sizes=True,
        size_format="human",
    )
    assert isinstance(response, dict)
    assert isinstance(response["databaseSize"], str)
    assert "indexes" in response
    assert any("internalDatabaseSizes" in index_stats for index_stats in response["indexes"].values())
