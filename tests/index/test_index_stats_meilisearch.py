from meilisearch.models import IndexStatsResults

def test_get_stats(empty_index):
    """Tests getting stats of an index."""
    response = empty_index().get_stats()
    assert isinstance(response, IndexStatsResults)
    assert response.number_of_documents == 0
