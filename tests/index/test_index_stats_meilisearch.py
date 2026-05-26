from meilisearch.models.index import IndexStats


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


def test_get_stats_with_internal_database_sizes(empty_index):
    """Tests getting stats with showInternalDatabaseSizes parameter."""
    response = empty_index().get_stats(show_internal_database_sizes=True)
    assert isinstance(response, IndexStats)
    assert response.number_of_documents == 0


def test_get_stats_with_size_format(empty_index):
    """Tests getting stats with sizeFormat parameter."""
    response = empty_index().get_stats(size_format="human")
    assert isinstance(response, IndexStats)
    assert response.number_of_documents == 0


def test_get_stats_with_all_params(empty_index):
    """Tests getting stats with both query parameters."""
    response = empty_index().get_stats(
        show_internal_database_sizes=True, size_format="human"
    )
    assert isinstance(response, IndexStats)
    assert response.number_of_documents == 0
