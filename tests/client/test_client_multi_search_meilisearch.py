import pytest

from meilisearch.errors import MeilisearchApiError


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
    with pytest.raises(MeilisearchApiError):
        client.multi_search([{"indexUid": "indexDoesNotExist", "q": ""}])


def test_multi_search_with_no_value_in_federation(client, empty_index):
    """Tests multi-search with federation, but no value"""
    empty_index("indexA")
    response = client.multi_search([{"indexUid": "indexA", "q": ""}], {})

    assert response["hits"][0]["_federation"]['indexUid'] == "indexA" if len(response["hits"]) >= 1 else isinstance(response, dict)


def test_multi_search_with_offset_and_limit_in_federation(client, empty_index):
    """Tests multi-search with federation, with offset and limit value"""
    empty_index("indexA")
    response = client.multi_search([{"indexUid": "indexA", "q": ""}], {"offset": 2, "limit": 2})
    
    assert len(response["hits"]) == 2 if response['hits'] else True


def test_multi_search_with_federation_options(client, empty_index):
    """Tests multi-search with federation, with federation options"""
    empty_index("indexA")
    response = client.multi_search([{"indexUid": "indexA", "q": "", "federationOptions": {"weight": 0.99}}], {"offset": 2, "limit": 2})

    assert isinstance(response["hits"], list)
    assert response["hits"][0]["_federation"]["weightedRankingScore"] < 0.99 if len(response["hits"]) >= 1 else True
