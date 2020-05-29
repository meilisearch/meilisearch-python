import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestKey:

    """ TESTS: key route """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)

    def test_get_keys(self):
        """Tests if public and private keys are generated and retrieved"""
        response = self.client.get_keys()
        assert isinstance(response, dict)
        assert 'public' in response
        assert 'private' in response
        assert response['public'] is not None
        assert response['private'] is not None
