import re

from meilisearch.models.index import IndexStats, SizeFormat

HUMAN_SIZE_PATTERN = re.compile(r"^\d+(\.\d+)?\s+(B|KiB|MiB|GiB|TiB)$")


def test_get_stats(empty_index):
    """Tests getting stats of an index."""
    response = empty_index().get_stats()
    assert isinstance(response, IndexStats)
    assert response.number_of_documents == 0


def test_get_stats_default(index_with_documents):
    """Tests getting stats of a non-empty index."""
    response = index_with_documents().get_stats()
    assert isinstance(response, IndexStats)
    assert response.number_of_documents == 31
    assert hasattr(response.field_distribution, "genre")
    assert response.field_distribution.genre == 11


def test_get_stats_with_internal_database_sizes(index_with_documents):
    """Tests getting stats with showInternalDatabaseSizes parameter."""
    response = index_with_documents().get_stats(show_internal_database_sizes=True)
    assert isinstance(response, IndexStats)
    assert response.internal_database_sizes is not None
    assert isinstance(response.internal_database_sizes, dict)
    assert len(response.internal_database_sizes) > 0
    assert all(isinstance(value, int) for value in response.internal_database_sizes.values())


def test_get_stats_with_size_format(index_with_documents):
    """Tests getting stats with sizeFormat parameter."""
    response = index_with_documents().get_stats(
        show_internal_database_sizes=True,
        size_format=SizeFormat.HUMAN,
    )
    assert isinstance(response, IndexStats)
    assert response.internal_database_sizes is not None
    assert all(
        isinstance(value, str) and HUMAN_SIZE_PATTERN.match(value)
        for value in response.internal_database_sizes.values()
    )


def test_get_stats_with_all_params(index_with_documents):
    """Tests getting stats with both query parameters."""
    response = index_with_documents().get_stats(
        show_internal_database_sizes=True,
        size_format="human",
    )
    assert isinstance(response, IndexStats)
    assert response.number_of_documents == 31
    assert response.internal_database_sizes is not None
    assert all(isinstance(value, str) for value in response.internal_database_sizes.values())
