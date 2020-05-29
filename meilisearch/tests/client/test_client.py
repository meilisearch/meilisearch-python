import pytest
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestClient:

    """ TESTS: Client class """

    @staticmethod
    def test_get_client():
        """Tests getting a client instance"""
        client = meilisearch.Client(BASE_URL, MASTER_KEY)
        assert client.config
        response = client.health()
        assert response.status_code == 200

    @staticmethod
    def test_get_client_without_master_key():
        """Tests getting a client instance without MASTER KEY"""
        client = meilisearch.Client(BASE_URL)
        with pytest.raises(Exception):
            client.get_version()

    @staticmethod
    def test_get_client_with_wrong_master_key():
        """Tests getting a client instance with an invalid MASTER KEY"""
        client = meilisearch.Client(BASE_URL, MASTER_KEY + "123")
        with pytest.raises(Exception):
            client.get_version()
