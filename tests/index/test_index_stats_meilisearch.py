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
    assert hasattr(response.field_distribution, 'genre')
    assert response.field_distribution.genre == 11
