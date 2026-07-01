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
def test_get_all_stats_human_size_format(client):
    """Tests getting all stats with human-formatted sizes."""
    response = client.get_all_stats(size_format="human")
    assert isinstance(response, dict)
    assert isinstance(response["databaseSize"], str)


@pytest.mark.usefixtures("indexes_sample")
def test_get_all_stats_internal_database_sizes(client):
    """Tests getting all stats with internal database sizes."""
    response = client.get_all_stats(show_internal_database_sizes=True)
    assert isinstance(response, dict)
    assert "internalDatabaseSizes" in response["indexes"]["indexUID"]
