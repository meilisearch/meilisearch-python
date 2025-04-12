import pytest

from meilisearch.errors import MeilisearchApiError
from tests.common import INDEX_UID, REMOTE_MS_1


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


def test_multi_search_with_no_value_in_federation(client, empty_index, index_with_documents):
    """Tests multi-search with federation, but no value"""
    index_with_documents()
    empty_index("indexB")
    response = client.multi_search(
        [{"indexUid": INDEX_UID, "q": ""}, {"indexUid": "indexB", "q": ""}], {}
    )
    assert "results" not in response
    assert len(response["hits"]) > 0
    assert "_federation" in response["hits"][0]
    assert response["limit"] == 20
    assert response["offset"] == 0


def test_multi_search_with_offset_and_limit_in_federation(client, index_with_documents):
    """Tests multi-search with federation, with offset and limit value"""
    index_with_documents()
    response = client.multi_search([{"indexUid": INDEX_UID, "q": ""}], {"offset": 2, "limit": 2})

    assert "results" not in response
    assert len(response["hits"]) == 2
    assert "_federation" in response["hits"][0]
    assert response["limit"] == 2
    assert response["offset"] == 2


def test_multi_search_with_federation_options(client, index_with_documents):
    """Tests multi-search with federation, with federation options"""
    index_with_documents()
    response = client.multi_search(
        [{"indexUid": INDEX_UID, "q": "", "federationOptions": {"weight": 0.99}}], {"limit": 2}
    )

    assert "results" not in response
    assert isinstance(response["hits"], list)
    assert len(response["hits"]) == 2
    assert response["hits"][0]["_federation"]["indexUid"] == INDEX_UID
    assert response["hits"][0]["_federation"]["weightedRankingScore"] >= 0.99
    assert response["limit"] == 2
    assert response["offset"] == 0


@pytest.mark.usefixtures("enable_network_options")
def test_multi_search_with_network(client, index_with_documents):
    """Tests multi-search with network, with federation options."""
    index_with_documents()
    response = client.multi_search(
        [{"indexUid": INDEX_UID, "q": "", "federationOptions": {"remote": REMOTE_MS_1}}],
        federation={},
    )

    assert "results" not in response
    assert isinstance(response["hits"], list)
    assert len(response["hits"]) >= 0
    assert response["hits"][0]["_federation"]["indexUid"] == INDEX_UID
    assert response["hits"][0]["_federation"]["remote"] == REMOTE_MS_1
    assert response["remoteErrors"] == {}
