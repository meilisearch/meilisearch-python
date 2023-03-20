import pytest

from meilisearch.errors import MeiliSearchApiError


def test_basic_multi_search(client, empty_index):
    """Tests multi-search on two indexes."""
    empty_index("indexA")
    empty_index("indexB")
    response = client.multi_search(
        [{"indexUid": "indexA", "q": ""}, {"indexUid": "indexB", "q": ""}]
    )

    assert isinstance(response, dict)
    assert response["results"][0]["indexUid"] == "indexA"
    assert response["results"][1]["indexUid"] == "indexB"
    assert response["results"][0]["limit"] == 20
    assert response["results"][1]["limit"] == 20


def test_multi_search_one_index(client, empty_index):
    """Tests multi-search on a simple query."""
    empty_index("indexA")
    response = client.multi_search([{"indexUid": "indexA", "q": ""}])

    assert isinstance(response, dict)
    assert response["results"][0]["indexUid"] == "indexA"
    assert response["results"][0]["limit"] == 20


def test_multi_search_on_no_index(client):
    """Tests multi-search on a non existing index."""
    with pytest.raises(MeiliSearchApiError):
        client.multi_search([{"indexUid": "indexDoesNotExist", "q": ""}])
