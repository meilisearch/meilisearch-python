import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestKey:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)

    def test_get_keys(self):
        response = self.client.get_keys()
        assert isinstance(response, dict)
        assert 'public' in response
        assert 'private' in response
