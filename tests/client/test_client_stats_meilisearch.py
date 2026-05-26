import pytest


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
def test_get_all_stats_with_params(client):
    """Tests getting all stats with query parameters."""
    response = client.get_all_stats(show_internal_database_sizes=True, size_format="human")
    assert isinstance(response, dict)
    assert "databaseSize" in response
    assert "indexes" in response
    for index_stats in response["indexes"].values():
        if "internalDatabaseSizes" in index_stats:
            assert isinstance(index_stats["internalDatabaseSizes"], dict)
