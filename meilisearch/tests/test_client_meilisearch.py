import pytest
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestClient:

    """ Client """
    @staticmethod
    def test_get_client():
        """Tests a call to get a client instance of MeiliSearch"""
        client = meilisearch.Client(BASE_URL, MASTER_KEY)
        assert client.config
        response = client.get_indexes()
        assert isinstance(response, list)

    @staticmethod
    def test_get_client_without_master_key():
        """Tests a call to get a client instance of MeiliSearch"""
        client = meilisearch.Client(BASE_URL)
        with pytest.raises(Exception):
            client.get_indexes()
